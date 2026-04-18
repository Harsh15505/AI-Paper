import pandas as pd

# Load the data
df = pd.read_csv("Ahmedabad_AQI_Daily.csv")

print("📊 DATA QUALITY CHECK")
print("="*80)
print(f"\nTotal records: {len(df)}")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")

print("\n📈 STATISTICAL SUMMARY:")
print("="*80)

for col in ['PM2_5', 'PM10', 'NO2']:
    if col in df.columns:
        print(f"\n{col}:")
        print(f"  Count:  {df[col].notna().sum()}")
        print(f"  Mean:   {df[col].mean():.2f}")
        print(f"  Std:    {df[col].std():.2f} {'✅ GOOD VARIANCE' if df[col].std() > 1.0 else '❌ NO VARIANCE'}")
        print(f"  Min:    {df[col].min():.2f}")
        print(f"  Max:    {df[col].max():.2f}")
        print(f"  Unique: {df[col].nunique()}")

print("\n" + "="*80)
print("🎯 VARIANCE CHECK:")
print("="*80)

all_good = True
for col in ['PM2_5', 'PM10', 'NO2']:
    if col in df.columns:
        std = df[col].std()
        if std < 1.0:
            print(f"❌ {col}: std = {std:.2f} - PROBLEMATIC (constant or near-constant)")
            all_good = False
        else:
            print(f"✅ {col}: std = {std:.2f} - GOOD for ML modeling")

if all_good:
    print("\n🎉 SUCCESS! All pollutants have sufficient variance for ML modeling!")
else:
    print("\n⚠️  WARNING: Some pollutants still have low variance")

print("\n📋 First 10 rows:")
print(df[['Date', 'PM2_5', 'PM10', 'NO2']].head(10))
