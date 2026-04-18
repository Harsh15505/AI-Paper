import requests
import pandas as pd
from datetime import datetime

# -----------------------------
# CONFIGURATION
# -----------------------------
API_KEY = "52e47f6a7447f56187977f1c352d9f149da0dd77e6a1303630356fd315de6b68"
LOCATION_ID = 228297

# Note: These sensors only have data from Feb 2025 onwards
DATETIME_FROM = "2025-02-18T00:00:00Z"  # When new sensors started
DATETIME_TO = "2026-02-16T23:59:59Z"  # Today's date

PARAMETERS = ["pm25", "pm10", "no2"]  # Parameters we want

headers = {
    "X-API-Key": API_KEY
}

# -----------------------------
# STEP 1: USE CORRECT SENSOR IDs
# -----------------------------
# Location 228297 has duplicate sensors - using the NEW active ones
print("Using active sensors from Ahmedabad location...")

sensor_map = {
    "no2": 12236582,   # NEW sensor (active Feb 2025+)
    "pm10": 12236584,  # NEW sensor (active Feb 2025+)
    "pm25": 12236585   # NEW sensor (active Feb 2025+)
}

print(f"Active sensors: {sensor_map}")

# -----------------------------
# STEP 2: FETCH DAILY MEASUREMENTS FOR EACH SENSOR
# -----------------------------
print("Starting measurement download...")

all_results = []

for param, sensor_id in sensor_map.items():
    print(f"Fetching data for {param} (sensor {sensor_id})...")
    
    # Use the /days endpoint for daily aggregated data
    url = f"https://api.openaq.org/v3/sensors/{sensor_id}/days"
    
    page = 1
    while True:
        print(f"  Page {page}...")
        
        params = {
            "datetime_from": DATETIME_FROM,
            "datetime_to": DATETIME_TO,
            "limit": 1000,
            "page": page
        }
        
        response = requests.get(url, headers=headers, params=params)
        
        if response.status_code != 200:
            print(f"  Error: {response.status_code}")
            print(f"  {response.text}")
            break
        
        data = response.json()
        results = data.get("results", [])
        
        if not results:
            break
        
        # Add parameter name to each result
        for result in results:
            result["parameter_name"] = param
        
        all_results.extend(results)
        page += 1

if not all_results:
    print("No data retrieved ❌")
    exit()

print("Download complete ✅")

# -----------------------------
# DATAFRAME
# -----------------------------
df = pd.DataFrame(all_results)

# Extract date from the period object
df["date"] = pd.to_datetime(df["period"].apply(lambda x: x["datetimeFrom"]["utc"]))
df["date"] = df["date"].dt.date

# Keep only date, parameter, and value
df = df[["date", "parameter_name", "value"]]

# -----------------------------
# PIVOT POLLUTANTS
# -----------------------------
pivot = df.pivot_table(
    index="date",
    columns="parameter_name",
    values="value"
).reset_index()

# Rename columns
column_mapping = {
    "date": "Date",
    "pm25": "PM2_5",
    "pm10": "PM10",
    "no2": "NO2"
}
pivot = pivot.rename(columns=column_mapping)

# Convert date to datetime
pivot["Date"] = pd.to_datetime(pivot["Date"])

# Sort by date
pivot = pivot.sort_values("Date").reset_index(drop=True)

# -----------------------------
# CLEAN MISSING VALUES
# -----------------------------
# Ensure we have all three columns
for col in ["PM2_5", "PM10", "NO2"]:
    if col not in pivot.columns:
        pivot[col] = None

pivot[["PM2_5", "PM10", "NO2"]] = (
    pivot[["PM2_5", "PM10", "NO2"]]
    .interpolate()
    .ffill()
)

# -----------------------------
# CREATE LAG FEATURES
# -----------------------------
pivot["PM2_5_Lag1"] = pivot["PM2_5"].shift(1)
pivot["PM2_5_Lag7"] = pivot["PM2_5"].rolling(7).mean()

pivot["PM10_Lag1"] = pivot["PM10"].shift(1)
pivot["PM10_Lag7"] = pivot["PM10"].rolling(7).mean()

pivot["NO2_Lag1"] = pivot["NO2"].shift(1)
pivot["NO2_Lag7"] = pivot["NO2"].rolling(7).mean()

pivot = pivot.dropna().reset_index(drop=True)

# -----------------------------
# SAVE CSV
# -----------------------------
pivot.to_csv("Ahmedabad_AQI_Daily.csv", index=False)

print("Saved → Ahmedabad_AQI_Daily.csv ✅")
print("All processing complete 🚀")
