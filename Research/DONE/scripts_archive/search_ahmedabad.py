import requests
import pandas as pd
from datetime import datetime, timezone, timedelta

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 Searching for ALL locations in Ahmedabad...\n")

# Search for Ahmedabad locations
url = "https://api.openaq.org/v3/locations"
params = {
    "limit": 1000,
    "country": "IN"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
all_locations = data.get("results", [])

# Filter for Ahmedabad
ahmedabad_locations = [
    loc for loc in all_locations 
    if "ahmedabad" in (loc.get("name") or "").lower() or 
       "ahmedabad" in (loc.get("locality") or "").lower()
]

print(f"Found {len(ahmedabad_locations)} locations in Ahmedabad\n")
print("="*120)

cutoff_recent = datetime.now(timezone.utc) - timedelta(days=30)

for loc in ahmedabad_locations:
    loc_id = loc.get("id")
    loc_name = loc.get("name")
    locality = loc.get("locality", "")
    sensors = loc.get("sensors", [])
    
    # Get sensor info
    sensor_info = {}
    for s in sensors:
        param_name = s["parameter"]["name"]
        sensor_info[param_name] = {
            "sensor_id": s["id"],
            "name": s["name"]
        }
    
    # Check last update
    last_update = loc.get("datetimeLast", {})
    first_update = loc.get("datetimeFirst", {})
    
    last_date_str = last_update.get("utc", "N/A") if last_update else "N/A"
    first_date_str = first_update.get("utc", "N/A") if first_update else "N/A"
    
    # Check if recent
    is_recent = False
    if last_update and "utc" in last_update:
        last_date = datetime.fromisoformat(last_update["utc"].replace("Z", "+00:00"))
        is_recent = last_date >= cutoff_recent
    
    status = "✅ ACTIVE" if is_recent else "❌ INACTIVE"
    
    print(f"\n📍 Location ID: {loc_id}")
    print(f"   Name: {loc_name}")
    print(f"   Locality: {locality}")
    print(f"   Status: {status}")
    print(f"   First Data: {first_date_str}")
    print(f"   Last Data:  {last_date_str}")
    print(f"   Available Sensors:")
    
    has_pm25 = "pm25" in sensor_info
    has_pm10 = "pm10" in sensor_info
    has_no2 = "no2" in sensor_info
    
    for param, info in sensor_info.items():
        marker = "✓" if param in ["pm25", "pm10", "no2"] else "•"
        print(f"      {marker} {param.upper()}: Sensor ID {info['sensor_id']}")
    
    # Check if has all three
    if has_pm25 and has_pm10 and has_no2:
        if is_recent:
            print(f"\n   🎯 HAS ALL THREE (PM2.5, PM10, NO2) - ACTIVE!")
        else:
            print(f"\n   ⚠️  HAS ALL THREE (PM2.5, PM10, NO2) - BUT INACTIVE")
    else:
        missing = []
        if not has_pm25: missing.append("PM2.5")
        if not has_pm10: missing.append("PM10")
        if not has_no2: missing.append("NO2")
        print(f"\n   ❌ Missing: {', '.join(missing)}")
    
    print("-"*120)

print("\n" + "="*120)
print("🏁 SEARCH COMPLETE")
print("="*120)
