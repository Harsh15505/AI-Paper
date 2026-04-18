import requests
import pandas as pd
from datetime import datetime, timezone

API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
headers = {"X-API-Key": API_KEY}

print("🔍 TESTING AHMEDABAD LOCATIONS FOR DEC 2024 - FEB 2025 DATA")
print("="*100)

# All Ahmedabad locations to test
locations_to_test = [
    228297,  # Current (SVPI Airport Hansol) - has Feb 2025+
    227533,
    228300,
    227534,
    5631
]

results_summary = []

for loc_id in locations_to_test:
    print(f"\n{'='*100}")
    print(f"📍 Testing Location ID: {loc_id}")
    print('='*100)
    
    # Get location details
    loc_url = f"https://api.openaq.org/v3/locations/{loc_id}"
    response = requests.get(loc_url, headers=headers)
    
    if response.status_code != 200:
        print(f"   ❌ Error: Location not found or API error ({response.status_code})")
        continue
    
    loc_data = response.json()
    loc = loc_data.get("results", [{}])[0]
    
    print(f"\n📋 Location Details:")
    print(f"   Name: {loc.get('name')}")
    print(f"   Locality: {loc.get('locality')}")
    print(f"   Country: {loc.get('country', {}).get('name')}")
    coords = loc.get('coordinates', {})
    print(f"   Coordinates: {coords.get('latitude', 'N/A'):.4f}, {coords.get('longitude', 'N/A'):.4f}")
    
    # Get sensors
    sensors = loc.get("sensors", [])
    sensor_map = {}
    for s in sensors:
        param = s.get("parameter", {}).get("name")
        if param in ["pm25", "pm10", "no2"]:
            sensor_map[param] = s.get("id")
    
    print(f"\n🔬 Available Sensors:")
    for param, sid in sensor_map.items():
        print(f"   {param.upper()}: Sensor ID {sid}")
    
    if len(sensor_map) != 3:
        missing = [p for p in ["pm25", "pm10", "no2"] if p not in sensor_map]
        print(f"\n   ❌ INCOMPLETE: Missing {', '.join(missing)}")
        continue
    
    # Test CRITICAL PERIOD: Dec 2024 - Feb 2025
    print(f"\n🎯 TESTING DEC 2024 - FEB 2025 (THE GAP PERIOD):")
    print("-"*100)
    
    gap_data = {}
    
    for param, sensor_id in sensor_map.items():
        test_url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
        test_params = {
            "datetime_from": "2024-12-01T00:00:00Z",
            "datetime_to": "2025-02-17T23:59:59Z",
            "limit": 200
        }
        
        resp = requests.get(test_url, headers=headers, params=test_params)
        
        if resp.status_code == 200:
            results = resp.json().get("results", [])
            
            if results:
                values = [r.get("value") for r in results]
                df_temp = pd.DataFrame({"value": values})
                
                first_date = results[0]["period"]["datetimeFrom"]["utc"][:10]
                last_date = results[-1]["period"]["datetimeFrom"]["utc"][:10]
                
                gap_data[param] = {
                    "days": len(results),
                    "first": first_date,
                    "last": last_date,
                    "mean": df_temp["value"].mean(),
                    "std": df_temp["value"].std(),
                    "min": df_temp["value"].min(),
                    "max": df_temp["value"].max()
                }
                
                print(f"   ✅ {param.upper():5s} | {len(results):3d} days | {first_date} → {last_date}")
                print(f"             Mean: {df_temp['value'].mean():6.1f} | Std: {df_temp['value'].std():6.2f} | Range: {df_temp['value'].min():.1f}-{df_temp['value'].max():.1f}")
            else:
                print(f"   ❌ {param.upper():5s} | No data in Dec 2024 - Feb 2025")
                gap_data[param] = None
    
    # Check if can fill gap
    has_all_gap = all(gap_data.get(p) is not None and gap_data[p]["days"] > 30 for p in ["pm25", "pm10", "no2"])
    
    if has_all_gap:
        print(f"\n   🎯 ✅ THIS LOCATION CAN FILL THE GAP!")
        print(f"   Coverage: All 3 pollutants have >30 days in Dec 2024 - Feb 2025")
        
        results_summary.append({
            "loc_id": loc_id,
            "name": loc.get('name'),
            "can_fill_gap": True,
            "gap_coverage": {k: v["days"] for k, v in gap_data.items() if v}
        })
    else:
        missing_gap = [p for p, v in gap_data.items() if v is None or v["days"] < 30]
        print(f"\n   ❌ Cannot fill gap (insufficient data for: {', '.join(missing_gap)})")
        
        results_summary.append({
            "loc_id": loc_id,
            "name": loc.get('name'),
            "can_fill_gap": False,
            "gap_coverage": {k: v["days"] if v else 0 for k, v in gap_data.items()}
        })

print("\n" + "="*100)
print("📊 FINAL SUMMARY - GAP FILLING CAPABILITY")
print("="*100)

gap_fillers = [r for r in results_summary if r["can_fill_gap"]]

if gap_fillers:
    print(f"\n✅ Found {len(gap_fillers)} location(s) that CAN FILL Dec 2024 - Feb 2025 gap:\n")
    for r in gap_fillers:
        print(f"   📍 Location {r['loc_id']}: {r['name']}")
        print(f"      Coverage: PM2.5={r['gap_coverage'].get('pm25', 0)}d, PM10={r['gap_coverage'].get('pm10', 0)}d, NO2={r['gap_coverage'].get('no2', 0)}d")
    
    print(f"\n🎯 RECOMMENDED STRATEGY:")
    print(f"   1. Use Location {gap_fillers[0]['loc_id']} for Dec 2024 - Feb 17, 2025")
    print(f"   2. Use Location 228297 for Feb 18, 2025 - Jan 2026")
    print(f"   3. This gives you FULL Dec 2024 - Jan 2026 coverage! ✅")
    
    print(f"\n⚠️  IMPORTANT: Check correlation between stations before merging")
    print(f"   (Will create correlation checker next)")
else:
    print("\n❌ None of the tested locations can fill Dec 2024 - Feb 2025 gap")
    print("\n💡 OPTIONS:")
    print("   1. Proceed with Feb 2025 - Jan 2026 only (safest)")
    print("   2. Request more Ahmedabad location IDs to test")
    print("   3. Use nearby cities (Gujarat) if scientifically justifiable")

print("\n" + "="*100)
