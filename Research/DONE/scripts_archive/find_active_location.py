import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 Searching for locations in India with active PM2.5, PM10, and NO2 sensors...\n")

# Search for locations in India
url = "https://api.openaq.org/v3/locations"
params = {
    "country": "IN",  # India
    "limit": 100,
    "parameters": "pm25,pm10,no2"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
locations = data.get("results", [])

print(f"Found {len(locations)} locations in India\n")

# Check each location for recent data
good_locations = []
from datetime import timezone
cutoff_date = datetime.now(timezone.utc) - timedelta(days=7)  # Active in last 7 days

for loc in locations:
    loc_id = loc.get("id")
    loc_name = loc.get("name")
    sensors = loc.get("sensors", [])
    
    # Check if has all three parameters
    params_found = {s["parameter"]["name"]: s["id"] for s in sensors}
    
    if "pm25" in params_found and "pm10" in params_found and "no2" in params_found:
        # Check last update date
        last_update = loc.get("datetimeLast", {})
        if last_update and "utc" in last_update:
            last_date = datetime.fromisoformat(last_update["utc"].replace("Z", "+00:00"))
            
            if last_date >= cutoff_date:
                good_locations.append({
                    "id": loc_id,
                    "name": loc_name,
                    "locality": loc.get("locality", ""),
                    "last_update": last_update["utc"],
                    "pm25_sensor": params_found["pm25"],
                    "pm10_sensor": params_found["pm10"],
                    "no2_sensor": params_found["no2"]
                })

print(f"\n✅ Found {len(good_locations)} locations with ALL THREE sensors active in last 7 days:\n")
print("="*100)

for i, loc in enumerate(good_locations[:10], 1):  # Show top 10
    print(f"{i}. Location ID: {loc['id']}")
    print(f"   Name: {loc['name']}, {loc['locality']}")
    print(f"   Last Update: {loc['last_update']}")
    print(f"   Sensors → PM2.5: {loc['pm25_sensor']}, PM10: {loc['pm10_sensor']}, NO2: {loc['no2_sensor']}")
    print("-"*100)

if good_locations:
    print(f"\n💡 RECOMMENDATION: Use Location ID {good_locations[0]['id']} ({good_locations[0]['name']})")
else:
    print("\n⚠️  No locations found with all three active sensors. Try:")
    print("   - Different country")
    print("   - Only PM2.5 data")
    print("   - Historical data from 2021-2022")
