import pandas as pd

# Load the analysis-ready dataset
df = pd.read_csv("Analysis_Ready_Dataset.csv")

print("📊 ANALYSIS-READY DATASET PREVIEW")
print("="*100)

print(f"\n📋 All Columns ({len(df.columns)}):")
for i, col in enumerate(df.columns, 1):
    print(f"   {i:2d}. {col}")

print(f"\n🔍 First Few Records:\n")
print(df.to_string())

print("\n" + "="*100)
print("✅ Dataset ready for modeling!")
print("\n💡 This includes:")
print("   ✓ Patient demographics")
print("   ✓ Pollution exposures (same day)")
print("   ✓ Lagged pollution (1-day & 7-day)")
print("   ✓ Seasonality controls (Month, Week, Season)")
print("   ✓ Outcome label (Respiratory_Label)")
