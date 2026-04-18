# 06 - AI Handoff Context (Copy/Paste)

Use this block when starting with a new AI assistant.

## Project Snapshot

- Domain: Pediatric respiratory admissions vs ambient air pollution
- Location: Ahmedabad
- Design: Retrospective observational
- Goal: Explainable ML model for respiratory admission prediction/association analysis

## Locked Decisions

- Age range: 2-12 years
- Study window: Feb 2025-Jan 2026
- AQI source: OpenAQ v3 sensor-based daily endpoint
- Pollution variables: PM2.5, PM10, NO2 (+ lag features)

## Final Title

Explainable Machine Learning for Predicting Respiratory-Related Pediatric Hospital Admissions Using Ambient Air Pollution Data: A Retrospective Study from an Urban Indian Hospital

## Data Targets

- Final usable rows: 1000-1200 preferred
- Respiratory target: ~250
- Non-respiratory target: ~800-1000

## Current Active Files

- AQI_Data_Collection.py
- prepare_analysis_dataset.py
- expand_patient_data.py
- qc_patient_data.py
- visualize_update.py
- PatientData.xlsx
- Ahmedabad_AQI_Daily.csv
- Analysis_Ready_Dataset.csv

## Archive Locations

- Research/DONE/scripts_archive/
- Research/DONE/data_backups/
- Research/DONE/notebooks_archive/
- Research/DONE/figures/

## What to Do Next

1. Continue adding patient records
2. Improve class balance with more non-respiratory controls
3. Rebuild analysis dataset regularly
4. Start/continue model training pipeline once sample size is sufficient
5. Keep docs updated when any locked decision changes
