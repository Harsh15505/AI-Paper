import requests
import pandas as pd
from datetime import datetime

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 Testing which sensors have data Nov 2024 - Feb 2026...\n")

test_sensors = {
    "NO2 (old)": 1315792,
    "NO2 (new)": 12236582,
    "PM10 (old)": 1315800,
    "PM10 (new)": 12236584,
    "PM2.5 (old)": 1315797,
    "PM2.5 (new)": 12236585
}

results = {}

for name, sensor_id in test_sensors.items():
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
    params = {
        "datetime_from": "2024-11-01T00:00:00Z",
        "datetime_to": "2026-02-16T23:59:59Z",
        "limit": 100
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code == 200:
        data = response.json()
        records = data.get("results", [])
        
        if records:
            values = [r.get("value") for r in records]
            df = pd.DataFrame({"value": values})
            
            first_date = records[0]["period"]["datetimeFrom"]["utc"]
            last_date = records[-1]["period"]["datetimeFrom"]["utc"]
            
            results[name] = {
                "sensor_id": sensor_id,
                "count": len(records),
                "mean": df["value"].mean(),
                "std": df["value"].std(),
                "min": df["value"].min(),
                "max": df["value"].max(),
                "first": first_date,
                "last": last_date
            }
            
            print(f"✅ {name} (ID: {sensor_id})")
            print(f"   Records: {len(records)}")
            print(f"   Mean: {df['value'].mean():.2f}, Std: {df['value'].std():.2f}")
            print(f"   Range: {df['value'].min():.2f} - {df['value'].max():.2f}")
            print(f"   Dates: {first_date[:10]} to {last_date[:10]}")
        else:
            print(f"❌ {name} (ID: {sensor_id})")
            print(f"   NO DATA in requested range")
    
    print()

print("\n" + "="*80)
print("📊 RECOMMENDATION:")
print("="*80)

# Determine which sensors to use
if "NO2 (new)" in results and results["NO2 (new)"]["count"] > 10:
    print(f"✅ Use NO2 Sensor: {test_sensors['NO2 (new)']} (NEW - has {results['NO2 (new)']['count']} days)")
elif "NO2 (old)" in results:
    print(f"⚠️  Use NO2 Sensor: {test_sensors['NO2 (old)']} (OLD)")

if "PM10 (new)" in results and results["PM10 (new)"]["count"] > 10:
    print(f"✅ Use PM10 Sensor: {test_sensors['PM10 (new)']} (NEW - has {results['PM10 (new)']['count']} days)")
elif "PM10 (old)" in results:
    print(f"⚠️  Use PM10 Sensor: {test_sensors['PM10 (old)']} (OLD)")

if "PM2.5 (new)" in results and results["PM2.5 (new)"]["count"] > 10:
    print(f"✅ Use PM2.5 Sensor: {test_sensors['PM2.5 (new)']} (NEW - has {results['PM2.5 (new)']['count']} days)")
elif "PM2.5 (old)" in results:
    print(f"⚠️  Use PM2.5 Sensor: {test_sensors['PM2.5 (old)']} (OLD)")
