import requests
from datetime import datetime, timezone, timedelta

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 Searching for locations with PM2.5, PM10, NO2 data from Dec 2024...\n")

# Get locations with all three parameters
url = "https://api.openaq.org/v3/locations"
params = {
    "country": "IN",
    "limit": 100,
    "parameters": "pm25,pm10,no2"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
locations = data.get("results", [])

print(f"Found {len(locations)} candidate locations in India\n")

target_date = datetime(2024, 12, 1, tzinfo=timezone.utc)
good_locations = []

for loc in locations:
    loc_id = loc.get("id")
    loc_name = loc.get("name")
    locality = loc.get("locality")
    sensors = loc.get("sensors", [])
    
    # Get sensor IDs for our parameters
    sensor_ids = {}
    for s in sensors:
        param = s.get("parameter", {}).get("name")
        if param in ["pm25", "pm10", "no2"]:
            sensor_ids[param] = s.get("id")
    
    # Must have all three
    if len(sensor_ids) != 3:
        continue
    
    # Check if each sensor has data from Dec 2024
    all_have_data = True
    sensor_counts = {}
    
    for param, sensor_id in sensor_ids.items():
        check_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
        check_params = {
            "datetime_from": "2024-12-01T00:00:00Z",
            "datetime_to": "2026-02-16T23:59:59Z",
            "limit": 1
        }
        
        resp = requests.get(check_url, headers=headers, params=check_params)
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            if not results:
                all_have_data = False
                break
            
            # Count total records
            count_params = {
                "datetime_from": "2024-12-01T00:00:00Z",
                "datetime_to": "2026-02-16T23:59:59Z",
                "limit": 1000
            }
            resp2 = requests.get(check_url, headers=headers, params=count_params)
            if resp2.status_code == 200:
                sensor_counts[param] = len(resp2.json().get("results", []))
        else:
            all_have_data = False
            break
    
    if all_have_data:
        good_locations.append({
            "id": loc_id,
            "name": loc_name,
            "locality": locality,
            "sensors": sensor_ids,
            "counts": sensor_counts
        })
        
        print(f"✅ Location {loc_id}: {loc_name}")
        print(f"   Locality: {locality}")
        print(f"   Data available: PM2.5({sensor_counts.get('pm25', 0)}d), PM10({sensor_counts.get('pm10', 0)}d), NO2({sensor_counts.get('no2', 0)}d)")
        print(f"   Sensors: {sensor_ids}")
        print()

print("\n" + "="*100)
print(f"📊 SUMMARY: Found {len(good_locations)} locations with ALL THREE sensors having Dec 2024+ data")
print("="*100)

if good_locations:
    print("\n🎯 TOP RECOMMENDATIONS:\n")
    for i, loc in enumerate(good_locations[:5], 1):
        avg_days = sum(loc['counts'].values()) / 3
        print(f"{i}. Location ID {loc['id']}: {loc['name']} ({loc['locality']})")
        print(f"   Average {avg_days:.0f} days of data per pollutant")
else:
    print("\n❌ No locations found with complete data from Dec 2024")
    print("🔍 Checking what date ranges ARE available for Ahmedabad alternatives...")
