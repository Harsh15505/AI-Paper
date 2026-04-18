# 04 - Data Pipeline and File Map

## Core Pipeline

1. Collect AQI daily data
   - Script: `AQI_Data_Collection.py`
   - Output: `Ahmedabad_AQI_Daily.csv`
2. Expand/maintain patient data
   - Script: `expand_patient_data.py` (as needed)
   - Working file: `PatientData.xlsx`
3. Quality check patient data
   - Script: `qc_patient_data.py`
4. Build merged analysis dataset
   - Script: `prepare_analysis_dataset.py`
   - Output: `Analysis_Ready_Dataset.csv`
5. Generate visual updates
   - Script: `visualize_update.py`

## Expected Key Columns (analysis-ready)

- Patient metadata:
  - Patient_ID
  - Age_Years
  - Gender
  - Respiratory_Label
  - Admission_Date
- Pollution features:
  - PM2_5, PM10, NO2 (current)
  - PM2_5_Lag1/7, PM10_Lag1/7, NO2_Lag1/7 (or equivalent naming)
- Temporal features:
  - Month
  - Week_of_Year
  - Season
  - Quarter
- Age stratification:
  - Age_Group

## Folder Hygiene Rules

- Keep active production scripts in root
- Move one-off debug/testing scripts to `Research/DONE/scripts_archive/`
- Move backup xlsx files to `Research/DONE/data_backups/`
- Move temporary notebooks to `Research/DONE/notebooks_archive/`
- Keep generated static figures in `Research/DONE/figures/`

## Current Directory Intent

Root directory should remain focused on:
- active code
- active data files
- final docs under `docs/`
