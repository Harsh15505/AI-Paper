import requests
import json
from datetime import datetime, timezone, timedelta

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 Checking Location 228297 details...\n")

# Get location details
url = f"https://api.openaq.org/v3/locations/228297"
response = requests.get(url, headers=headers)

if response.status_code != 200:
    print(f"❌ Error: {response.status_code}")
    print(response.text)
else:
    data = response.json()
    loc = data.get("results", [{}])[0]
    
    print(f"📍 Location ID: {loc.get('id')}")
    print(f"   Name: {loc.get('name')}")
    print(f"   Locality: {loc.get('locality')}")
    print(f"   Country: {loc.get('country', {}).get('name')}")
    print(f"   Timezone: {loc.get('timezone')}")
    print(f"   Coordinates: {loc.get('coordinates')}")
    
    first_update = loc.get("datetimeFirst", {})
    last_update = loc.get("datetimeLast", {})
    
    print(f"\n📅 Data Timeline:")
    print(f"   First Data: {first_update.get('utc', 'N/A')}")
    print(f"   Last Data:  {last_update.get('utc', 'N/A')}")
    
    print(f"\n🔬 Available Sensors:")
    sensors = loc.get("sensors", [])
    
    cutoff_recent = datetime.now(timezone.utc) - timedelta(days=30)
    
    for sensor in sensors:
        param = sensor.get("parameter", {})
        sensor_id = sensor.get("id")
        param_name = param.get("name")
        
        print(f"\n   📊 {param_name.upper()}")
        print(f"      Sensor ID: {sensor_id}")
        print(f"      Units: {param.get('units')}")
        print(f"      Display Name: {param.get('displayName')}")
    
    # Now check date ranges for each sensor
    print(f"\n🔍 Checking actual data availability for each sensor...")
    print("="*100)
    
    for sensor in sensors:
        param_name = sensor.get("parameter", {}).get("name")
        sensor_id = sensor.get("id")
        
        if param_name in ["pm25", "pm10", "no2"]:
            # Check recent data
            url_check = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
            params = {
                "datetime_from": "2024-11-01T00:00:00Z",
                "datetime_to": "2026-02-16T23:59:59Z",
                "limit": 1
            }
            
            resp = requests.get(url_check, headers=headers, params=params)
            if resp.status_code == 200:
                results = resp.json().get("results", [])
                if results:
                    date_range = results[0]["period"]["datetimeFrom"]["utc"]
                    print(f"\n✅ {param_name.upper()} (Sensor {sensor_id})")
                    print(f"   Has data in Nov 2024 - Feb 2026 range")
                    print(f"   Sample date: {date_range}")
                else:
                    print(f"\n❌ {param_name.upper()} (Sensor {sensor_id})")
                    print(f"   NO DATA in Nov 2024 - Feb 2026 range")
                    
                    # Check what date range it does have
                    url_any = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
                    params_any = {"limit": 1, "sort": "desc"}
                    resp_any = requests.get(url_any, headers=headers, params=params_any)
                    
                    if resp_any.status_code == 200:
                        results_any = resp_any.json().get("results", [])
                        if results_any:
                            last_date = results_any[0]["period"]["datetimeFrom"]["utc"]
                            print(f"   Last available data: {last_date}")

print("\n" + "="*100)

# Now search for other locations with "Ahmedabad" or city name variations
print("\n\n🔍 Searching for Gujarat locations...\n")

url = "https://api.openaq.org/v3/locations"
params = {
    "limit": 1000,
    "country": "IN"
}

response = requests.get(url, headers=headers, params=params)
data = response.json()
all_locations = data.get("results", [])

# Search for Gujarat or coordinates near Ahmedabad (23.0225° N, 72.5714° E)
gujarat_keywords = ["gujarat", "gandhinagar", "vadodara", "surat", "rajkot"]
potential = []

for loc in all_locations:
    name = (loc.get("name") or "").lower()
    locality = (loc.get("locality") or "").lower()
    
    # Check keywords or coordinates near Ahmedabad
    coords = loc.get("coordinates", {})
    lat = coords.get("latitude", 0) if coords else 0
    lon = coords.get("longitude", 0) if coords else 0
    
    # Ahmedabad is around 23.02°N, 72.57°E - check within ~2 degrees
    near_ahmedabad = (21 <= lat <= 25) and (70 <= lon <= 75)
    
    has_keyword = any(kw in name or kw in locality for kw in gujarat_keywords)
    
    if near_ahmedabad or has_keyword:
        potential.append({
            "id": loc.get("id"),
            "name": loc.get("name"),
            "locality": loc.get("locality"),
            "coords": f"{lat:.2f}, {lon:.2f}",
            "sensors": [s.get("parameter", {}).get("name") for s in loc.get("sensors", [])]
        })

print(f"Found {len(potential)} locations in Gujarat/near Ahmedabad:")
for p in potential[:15]:
    sensors_str = ", ".join(p["sensors"])
    print(f"\n   ID {p['id']}: {p['name']} ({p['locality']})")
    print(f"   Coords: {p['coords']}")
    print(f"   Sensors: {sensors_str}")
