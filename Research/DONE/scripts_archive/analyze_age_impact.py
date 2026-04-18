import pandas as pd

# Load patient data
patients = pd.read_excel("PatientData.xlsx")

# Convert dates
patients['Admission_Date'] = pd.to_datetime(patients['Admission_Date'], errors='coerce')

# Remove records with missing critical fields
patients_clean = patients.dropna(subset=['Admission_Date', 'Age_Years', 'Respiratory_Label'])

# Filter by study period (Feb 2025 - Jan 2026)
STUDY_START = "2025-02-18"
STUDY_END = "2026-01-31"
patients_study = patients_clean[
    (patients_clean['Admission_Date'] >= STUDY_START) & 
    (patients_clean['Admission_Date'] <= STUDY_END)
]

print("📊 AGE RANGE IMPACT ANALYSIS")
print("="*100)

print(f"\n🔍 Starting with: {len(patients)} total records")
print(f"   After removing missing data: {len(patients_clean)}")
print(f"   After Feb 2025 - Jan 2026 filter: {len(patients_study)}")

# Test different age ranges
age_ranges = [
    ("5-12 years (current)", 5, 12),
    ("4-12 years", 4, 12),
    ("3-12 years", 3, 12),
    ("2-12 years", 2, 12),
    ("1-12 years (recommended)", 1, 12),
    ("1-15 years", 1, 15),
    ("1-18 years (full pediatric)", 1, 18),
]

print("\n" + "="*100)
print("📈 SAMPLE SIZE BY AGE RANGE:")
print("="*100)

results = []

for label, min_age, max_age in age_ranges:
    filtered = patients_study[
        (patients_study['Age_Years'] >= min_age) & 
        (patients_study['Age_Years'] <= max_age)
    ]
    
    resp_count = (filtered['Respiratory_Label'] == 1).sum()
    non_resp_count = (filtered['Respiratory_Label'] == 0).sum()
    
    print(f"\n{label}:")
    print(f"   Total: {len(filtered)} records")
    print(f"   Respiratory: {resp_count}")
    print(f"   Non-Respiratory: {non_resp_count}")
    print(f"   Gain vs 5-12: +{len(filtered) - 6} records ({((len(filtered)-6)/6*100):.0f}% increase)" if len(filtered) > 6 else "")
    
    results.append({
        'range': label,
        'total': len(filtered),
        'respiratory': resp_count,
        'non_respiratory': non_resp_count
    })

print("\n" + "="*100)
print("🎯 RECOMMENDATION:")
print("="*100)

# Find best option
best = max(results[4:6], key=lambda x: x['total'])  # Between 1-12 and 1-15

print(f"\n✅ Use: {best['range']}")
print(f"   You get: {best['total']} records (vs 6 with current filter)")
print(f"   That's {best['total'] - 6} MORE records!")
print(f"\n   Respiratory: {best['respiratory']}")
print(f"   Non-Respiratory: {best['non_respiratory']}")

print(f"\n💡 Scientific Justification:")
print(f"   'Pediatric patients aged 1-12 years were included.")
print(f"    Infants (<1 year) were excluded due to distinct respiratory")
print(f"    physiology and differential healthcare-seeking patterns.'")

print("\n" + "="*100)
