"""
Complete Data Merge & Feature Engineering Pipeline
=================================================
Combines patient records with pollution data and adds temporal features

Usage: Run this script whenever you get new patient data batches
"""

import pandas as pd
import numpy as np
from datetime import datetime

print("🚀 STARTING DATA PREPARATION PIPELINE")
print("="*100)

# =============================================================================
# CONFIGURATION
# =============================================================================

STUDY_START_DATE = "2025-02-18"  # When pollution sensors started
STUDY_END_DATE = "2026-01-31"    # End of study period
MIN_AGE = 2                       # Minimum age (years) - excludes infants
MAX_AGE = 12                      # Maximum age (years) - pre-adolescent

PATIENT_FILE = "PatientData.xlsx"
POLLUTION_FILE = "Ahmedabad_AQI_Daily.csv"
OUTPUT_FILE = "Analysis_Ready_Dataset.csv"

# =============================================================================
# STEP 1: LOAD PATIENT DATA
# =============================================================================

print("\n📂 STEP 1: Loading Patient Data...")
print("-"*100)

try:
    patients = pd.read_excel(PATIENT_FILE)
    print(f"✅ Loaded {len(patients)} patient records")
    print(f"   Columns: {', '.join(patients.columns)}")
except Exception as e:
    print(f"❌ Error loading patient data: {e}")
    exit()

# =============================================================================
# STEP 2: CLEAN AND FILTER PATIENT DATA
# =============================================================================

print("\n🧹 STEP 2: Cleaning Patient Data...")
print("-"*100)

initial_count = len(patients)

# Convert dates
patients['Admission_Date'] = pd.to_datetime(patients['Admission_Date'], errors='coerce')

# Remove records with missing critical fields
patients_clean = patients.dropna(subset=['Admission_Date', 'Age_Years', 'Respiratory_Label'])
print(f"   Removed {initial_count - len(patients_clean)} records with missing critical data")

# Filter by age (2-12 years only)
patients_clean = patients_clean[
    (patients_clean['Age_Years'] >= MIN_AGE) & 
    (patients_clean['Age_Years'] <= MAX_AGE)
]
print(f"   Removed {len(patients) - initial_count - len(patients_clean)} records outside age range (2-12 years)")

# Filter by study period
patients_clean = patients_clean[
    (patients_clean['Admission_Date'] >= STUDY_START_DATE) & 
    (patients_clean['Admission_Date'] <= STUDY_END_DATE)
]
print(f"   Removed records outside study period (Feb 2025 - Jan 2026)")

print(f"\n✅ Clean dataset: {len(patients_clean)} records")
print(f"   Respiratory (1): {(patients_clean['Respiratory_Label'] == 1).sum()}")
print(f"   Non-Respiratory (0): {(patients_clean['Respiratory_Label'] == 0).sum()}")

if len(patients_clean) == 0:
    print("❌ No records remaining after filtering!")
    exit()

# =============================================================================
# STEP 3: LOAD POLLUTION DATA
# =============================================================================

print("\n📂 STEP 3: Loading Pollution Data...")
print("-"*100)

try:
    pollution = pd.read_csv(POLLUTION_FILE)
    pollution['Date'] = pd.to_datetime(pollution['Date'])
    print(f"✅ Loaded {len(pollution)} days of pollution data")
    print(f"   Date range: {pollution['Date'].min()} to {pollution['Date'].max()}")
    print(f"   Variables: PM2.5, PM10, NO2 + lag features")
except Exception as e:
    print(f"❌ Error loading pollution data: {e}")
    exit()

# =============================================================================
# STEP 4: MERGE PATIENT + POLLUTION DATA
# =============================================================================

print("\n🔗 STEP 4: Merging Patient and Pollution Data...")
print("-"*100)

# Create date-only column for merging
patients_clean['Date'] = patients_clean['Admission_Date'].dt.date
pollution['Date_Key'] = pollution['Date'].dt.date

# Merge on date
merged = patients_clean.merge(
    pollution,
    left_on='Date',
    right_on='Date_Key',
    how='left',
    suffixes=('', '_pollution')
)

# Check merge quality
unmatched = merged['PM2_5'].isna().sum()
if unmatched > 0:
    print(f"⚠️  WARNING: {unmatched} records have no matching pollution data")
    print(f"   These dates may be outside pollution data range")
    
    # Show which dates are missing
    missing_dates = merged[merged['PM2_5'].isna()]['Admission_Date'].dt.date.unique()
    if len(missing_dates) <= 10:
        print(f"   Missing dates: {missing_dates}")
else:
    print(f"✅ All {len(merged)} records successfully merged with pollution data")

# Remove unmatched records
merged = merged.dropna(subset=['PM2_5', 'PM10', 'NO2'])
print(f"   Final merged dataset: {len(merged)} records")

# =============================================================================
# STEP 5: ADD SEASONALITY FEATURES
# =============================================================================

print("\n📅 STEP 5: Adding Seasonality & Temporal Features...")
print("-"*100)

# Extract date components
merged['Year'] = merged['Admission_Date'].dt.year
merged['Month'] = merged['Admission_Date'].dt.month
merged['Week_of_Year'] = merged['Admission_Date'].dt.isocalendar().week
merged['Day_of_Week'] = merged['Admission_Date'].dt.dayofweek  # 0=Monday, 6=Sunday
merged['Day_of_Year'] = merged['Admission_Date'].dt.dayofyear

# Season (India-specific)
def get_season(month):
    if month in [12, 1, 2]:
        return 'Winter'
    elif month in [3, 4, 5]:
        return 'Summer'
    elif month in [6, 7, 8, 9]:
        return 'Monsoon'
    else:  # 10, 11
        return 'Post-Monsoon'

merged['Season'] = merged['Month'].apply(get_season)

# Quarter
merged['Quarter'] = merged['Admission_Date'].dt.quarter

# Age Group (for sensitivity analyses)
merged['Age_Group'] = pd.cut(
    merged['Age_Years'],
    bins=[2, 5, 8, 12],
    labels=['Toddler (2-4)', 'Young (5-7)', 'Older (8-12)'],
    include_lowest=True
)

print(f"✅ Added temporal features:")
print(f"   - Year, Month, Week_of_Year, Day_of_Week, Day_of_Year")
print(f"   - Season (India-specific: Winter/Summer/Monsoon/Post-Monsoon)")
print(f"   - Quarter")
print(f"   - Age_Group (Toddler 2-4, Young 5-7, Older 8-12)")

# =============================================================================
# STEP 6: SELECT FINAL COLUMNS
# =============================================================================

print("\n📋 STEP 6: Selecting Final Analysis Columns...")
print("-"*100)

# Define final column set
final_columns = [
    # Patient identifiers & demographics
    'Patient_ID',
    'Age_Years',
    'Gender',
    'Admission_Date',
    
    # Outcome variable
    'Respiratory_Label',
    
    # Current day pollution
    'PM2_5',
    'PM10',
    'NO2',
    
    # Lagged pollution features
    'PM2_5_Lag1',
    'PM2_5_Lag7',
    'PM10_Lag1',
    'PM10_Lag7',
    'NO2_Lag1',
    'NO2_Lag7',
    
    # Temporal features (for confounding control)
    'Month',
    'Week_of_Year',
    'Day_of_Week',
    'Season',
    'Quarter',
    'Age_Group',
    
    # Optional: keep for reference
    'Primary_Diagnosis',
    'Locality'
]

# Keep only columns that exist
final_columns = [col for col in final_columns if col in merged.columns]
merged_final = merged[final_columns].copy()

print(f"✅ Final dataset has {len(final_columns)} columns")

# =============================================================================
# STEP 7: DATA QUALITY REPORT
# =============================================================================

print("\n📊 STEP 7: Final Data Quality Report")
print("="*100)

print(f"\n📈 Sample Size:")
print(f"   Total Records: {len(merged_final)}")
print(f"   Respiratory (1): {(merged_final['Respiratory_Label'] == 1).sum()} ({(merged_final['Respiratory_Label'] == 1).sum()/len(merged_final)*100:.1f}%)")
print(f"   Non-Respiratory (0): {(merged_final['Respiratory_Label'] == 0).sum()} ({(merged_final['Respiratory_Label'] == 0).sum()/len(merged_final)*100:.1f}%)")

print(f"\n📅 Temporal Coverage:")
print(f"   Date Range: {merged_final['Admission_Date'].min().date()} to {merged_final['Admission_Date'].max().date()}")
print(f"   Span: {(merged_final['Admission_Date'].max() - merged_final['Admission_Date'].min()).days} days")

print(f"\n👥 Demographics:")
print(f"   Age: {merged_final['Age_Years'].min():.0f}-{merged_final['Age_Years'].max():.0f} years (Mean: {merged_final['Age_Years'].mean():.1f})")
if 'Gender' in merged_final.columns:
    gender_dist = merged_final['Gender'].value_counts()
    for gender, count in gender_dist.items():
        print(f"   Gender {gender}: {count} ({count/len(merged_final)*100:.1f}%)")
if 'Age_Group' in merged_final.columns:
    print(f"\n   Age Group Distribution:")
    age_group_dist = merged_final['Age_Group'].value_counts().sort_index()
    for group, count in age_group_dist.items():
        print(f"      {group}: {count} ({count/len(merged_final)*100:.1f}%)")

print(f"\n🏭 Pollution Summary:")
for var in ['PM2_5', 'PM10', 'NO2']:
    if var in merged_final.columns:
        print(f"   {var}: Mean={merged_final[var].mean():.1f}, Std={merged_final[var].std():.1f}, Range={merged_final[var].min():.1f}-{merged_final[var].max():.1f}")

print(f"\n🌦️  Seasonal Distribution:")
if 'Season' in merged_final.columns:
    season_dist = merged_final['Season'].value_counts()
    for season, count in season_dist.items():
        print(f"   {season}: {count} ({count/len(merged_final)*100:.1f}%)")

print(f"\n⚠️  Missing Data:")
missing = merged_final.isnull().sum()
missing = missing[missing > 0]
if len(missing) > 0:
    for col, count in missing.items():
        print(f"   {col}: {count} ({count/len(merged_final)*100:.1f}%)")
else:
    print("   ✅ No missing data in critical variables!")

# =============================================================================
# STEP 8: SAVE OUTPUT
# =============================================================================

print(f"\n💾 STEP 8: Saving Analysis-Ready Dataset...")
print("-"*100)

try:
    merged_final.to_csv(OUTPUT_FILE, index=False)
    print(f"✅ Saved to: {OUTPUT_FILE}")
    print(f"   Records: {len(merged_final)}")
    print(f"   Columns: {len(merged_final.columns)}")
except Exception as e:
    print(f"❌ Error saving file: {e}")

print("\n" + "="*100)
print("🎉 DATA PREPARATION COMPLETE!")
print("="*100)
print(f"\n📊 Ready for modeling: {OUTPUT_FILE}")
print(f"\n💡 Next Steps:")
print(f"   1. Explore data (distributions, correlations)")
print(f"   2. Split train/test (stratified by Respiratory_Label)")
print(f"   3. Train models (Logistic Regression, Random Forest)")
print(f"   4. Generate SHAP explanations")
print("\n" + "="*100)
