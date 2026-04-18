import requests
import pandas as pd
from datetime import datetime, timezone

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 TESTING MULTIPLE AHMEDABAD LOCATIONS FOR DEC 2024 - FEB 2025 GAP")
print("="*100)

# Add your location IDs here
# Currently we know: 228297 (SVPI Airport Hansol)
# The user said they have more location codes for Ahmedabad

test_locations = [
    228297,  # Current one (SVPI Airport Hansol)
    # Add more location IDs below when user provides them
]

print("\n📍 Please provide additional Ahmedabad location IDs to test")
print("   Format: Just the numeric ID (e.g., 228297)")
print("\n   Waiting for location IDs...\n")

# For now, let's search for any Ahmedabad-related locations
print("🔍 Searching OpenAQ database for Ahmedabad locations...\n")

# Search by coordinates (Ahmedabad area: ~23°N, ~72.5°E)
search_url = "https://api.openaq.org/v3/locations"
params = {
    "coordinates": "23.02,72.57",
    "radius": 30000,  # 30km radius
    "limit": 100
}

response = requests.get(search_url, headers=headers, params=params)

if response.status_code == 200:
    data = response.json()
    locations = data.get("results", [])
    
    print(f"Found {len(locations)} locations within 30km of Ahmedabad center\n")
    
    ahmedabad_locations = []
    
    for loc in locations:
        loc_id = loc.get("id")
        name = loc.get("name", "")
        locality = loc.get("locality") or ""
        coords = loc.get("coordinates", {})
        sensors = loc.get("sensors", [])
        
        # Get sensor parameters
        params_avail = [s.get("parameter", {}).get("name") for s in sensors]
        has_all_three = all(p in params_avail for p in ["pm25", "pm10", "no2"])
        
        if has_all_three:
            ahmedabad_locations.append({
                "id": loc_id,
                "name": name,
                "locality": locality,
                "lat": coords.get("latitude"),
                "lon": coords.get("longitude"),
                "sensors": {s.get("parameter", {}).get("name"): s.get("id") for s in sensors if s.get("parameter", {}).get("name") in ["pm25", "pm10", "no2"]}
            })
    
    print(f"✅ Found {len(ahmedabad_locations)} locations with PM2.5, PM10, AND NO2")
    print("="*100)
    
    for loc in ahmedabad_locations:
        print(f"\n📍 Location ID: {loc['id']}")
        print(f"   Name: {loc['name']}")
        print(f"   Locality: {loc['locality']}")
        print(f"   Coordinates: {loc['lat']:.4f}, {loc['lon']:.4f}")
        print(f"   Sensors: PM2.5={loc['sensors'].get('pm25')}, PM10={loc['sensors'].get('pm10')}, NO2={loc['sensors'].get('no2')}")
        
        # Test for Dec 2024 - Feb 2025 data
        print(f"\n   🔍 Testing Dec 2024 - Feb 2025 availability:")
        
        has_dec_data = {}
        for param, sensor_id in loc['sensors'].items():
            if param in ["pm25", "pm10", "no2"]:
                test_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
                test_params = {
                    "datetime_from": "2024-12-01T00:00:00Z",
                    "datetime_to": "2025-02-17T23:59:59Z",
                    "limit": 100
                }
                
                resp = requests.get(test_url, headers=headers, params=test_params)
                if resp.status_code == 200:
                    results = resp.json().get("results", [])
                    has_dec_data[param] = len(results)
                    
                    if results:
                        first_date = results[0]["period"]["datetimeFrom"]["utc"][:10]
                        last_date = results[-1]["period"]["datetimeFrom"]["utc"][:10]
                        
                        values = [r.get("value") for r in results]
                        mean = sum(values) / len(values) if values else 0
                        
                        print(f"      ✅ {param.upper()}: {len(results)} days | {first_date} to {last_date} | Mean: {mean:.1f}")
                    else:
                        print(f"      ❌ {param.upper()}: No data")
        
        # Check if this location fills the gap
        if all(has_dec_data.get(p, 0) > 30 for p in ["pm25", "pm10", "no2"]):
            print(f"\n   🎯 ✅ THIS LOCATION CAN FILL DEC 2024 - FEB 2025 GAP!")
        elif any(has_dec_data.get(p, 0) > 0 for p in ["pm25", "pm10", "no2"]):
            print(f"\n   ⚠️  Partial data available")
        else:
            print(f"\n   ❌ No Dec 2024 - Feb 2025 data")
        
        print("-"*100)

print("\n" + "="*100)
print("📊 RECOMMENDATIONS:")
print("="*100)
print("\nIf multiple stations have Dec 2024 - Feb 2025 data:")
print("✅ Use station-specific data for respective periods")
print("✅ Create composite pollution dataset covering full Dec 2024 - Jan 2026")
print("✅ Note stations used in methods section")
print("\n⚠️  Check for consistency: Stations should have similar pollution levels")
print("   (correlation between stations should be r > 0.7)")
