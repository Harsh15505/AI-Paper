import requests
import pandas as pd

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
LOCATION_ID = 228297

DATETIME_FROM = "2024-11-01T00:00:00Z"
DATETIME_TO = "2026-02-16T23:59:59Z"

PARAMETERS = ["pm25", "pm10", "no2"]

headers = {
    "X-API-Key": API_KEY
}

# -----------------------------
# GET SENSOR IDs
# -----------------------------
print("🔍 DIAGNOSTIC CHECK - Fetching location details...\n")

location_url = f"https://api.openaq.org/v3/locations/{LOCATION_ID}"
response = requests.get(location_url, headers=headers)

location_data = response.json()
sensors = location_data.get("results", [{}])[0].get("sensors", [])

sensor_map = {}
for sensor in sensors:
    param_name = sensor.get("parameter", {}).get("name")
    if param_name in PARAMETERS:
        sensor_map[param_name] = sensor.get("id")

print(f"Sensors found: {sensor_map}\n")

# -----------------------------
# CHECK RAW DATA FOR EACH SENSOR
# -----------------------------

for param, sensor_id in sensor_map.items():
    print(f"\n{'='*60}")
    print(f"📊 PARAMETER: {param} (Sensor ID: {sensor_id})")
    print(f"{'='*60}")
    
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
    
    params = {
        "datetime_from": DATETIME_FROM,
        "datetime_to": DATETIME_TO,
        "limit": 1000,
        "page": 1
    }
    
    response = requests.get(url, headers=headers, params=params)
    
    if response.status_code != 200:
        print(f"❌ Error: {response.status_code}")
        continue
    
    data = response.json()
    results = data.get("results", [])
    
    print(f"\n📈 Total records fetched (page 1): {len(results)}")
    
    if results:
        # Extract values
        values = [r.get("value") for r in results[:20]]  # First 20
        
        print(f"\n🔢 First 20 values:")
        print(values)
        
        # Calculate statistics
        all_values = [r.get("value") for r in results]
        df_temp = pd.DataFrame({"value": all_values})
        
        print(f"\n📊 Statistics (all records on page 1):")
        print(f"   Count:  {df_temp['value'].count()}")
        print(f"   Mean:   {df_temp['value'].mean():.2f}")
        print(f"   Std:    {df_temp['value'].std():.6f}")
        print(f"   Min:    {df_temp['value'].min():.2f}")
        print(f"   Max:    {df_temp['value'].max():.2f}")
        print(f"   Unique: {df_temp['value'].nunique()}")
        
        # Check if constant
        if df_temp['value'].nunique() == 1:
            print(f"\n🚨 WARNING: ALL VALUES ARE IDENTICAL ({df_temp['value'].iloc[0]})")
        elif df_temp['value'].std() < 0.01:
            print(f"\n⚠️  WARNING: Very low variance (std = {df_temp['value'].std():.6f})")
        else:
            print(f"\n✅ Values are varying normally")
            
        # Show date range
        if len(results) > 0:
            first_date = results[0]["period"]["datetimeFrom"]["utc"]
            last_date = results[-1]["period"]["datetimeFrom"]["utc"]
            print(f"\n📅 Date range:")
            print(f"   First: {first_date}")
            print(f"   Last:  {last_date}")

print("\n" + "="*60)
print("🏁 DIAGNOSTIC COMPLETE")
print("="*60)
