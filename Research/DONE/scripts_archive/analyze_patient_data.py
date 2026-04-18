import pandas as pd

# Load patient data
df = pd.read_excel("PatientData.xlsx")

print("📊 PATIENT DATA STRUCTURE ANALYSIS")
print("="*80)

print(f"\n📈 Dataset Size:")
print(f"   Total Records: {len(df)}")
print(f"   Total Columns: {len(df.columns)}")

print(f"\n📋 Column Names:")
for i, col in enumerate(df.columns, 1):
    print(f"   {i}. {col}")

print(f"\n🔍 Data Types:")
print(df.dtypes)

print(f"\n📊 First 10 Rows:")
print(df.head(10))

print(f"\n🔢 Respiratory Label Distribution:")
if 'Respiratory_Label' in df.columns:
    print(df['Respiratory_Label'].value_counts())
    print(f"\n   Total Respiratory (1): {(df['Respiratory_Label'] == 1).sum()}")
    print(f"   Total Non-Respiratory (0): {(df['Respiratory_Label'] == 0).sum()}")
    print(f"   Percentage Respiratory: {(df['Respiratory_Label'] == 1).sum() / len(df) * 100:.1f}%")

print(f"\n🗓️ Date Range:")
if 'Admission_Date' in df.columns:
    df['Admission_Date'] = pd.to_datetime(df['Admission_Date'], errors='coerce')
    print(f"   First Admission: {df['Admission_Date'].min()}")
    print(f"   Last Admission: {df['Admission_Date'].max()}")
    print(f"   Date span: {(df['Admission_Date'].max() - df['Admission_Date'].min()).days} days")

print(f"\n⚠️ Missing Values:")
missing = df.isnull().sum()
missing = missing[missing > 0]
if len(missing) > 0:
    for col, count in missing.items():
        print(f"   {col}: {count} ({count/len(df)*100:.1f}%)")
else:
    print("   No missing values")

print(f"\n👥 Demographics:")
if 'Age_Years' in df.columns:
    print(f"   Age Range: {df['Age_Years'].min():.0f} - {df['Age_Years'].max():.0f} years")
    print(f"   Mean Age: {df['Age_Years'].mean():.1f} years")
if 'Gender' in df.columns:
    print(f"   Gender Distribution:")
    print(df['Gender'].value_counts())

print("\n" + "="*80)
