# 00 - Master Context (Single Source of Truth)

## Research Title (Final)

**Explainable Machine Learning for Predicting Respiratory-Related Pediatric Hospital Admissions Using Ambient Air Pollution Data: A Retrospective Study from an Urban Indian Hospital**

## Objective

Develop an explainable ML framework to analyze/predict respiratory-related pediatric hospital admissions using ambient pollution exposure features.

## Locked Scope

- Population: Pediatric inpatients
- Age inclusion: 2-12 years
- Study window: Feb 2025-Jan 2026
- Geography: Ahmedabad
- Outcome: Respiratory vs non-respiratory admission label

## Why Scope Is Locked

- Usable AQI data is effectively available from Feb 2025 onward for selected OpenAQ sensors in this workflow
- Earlier data availability is inconsistent due station/sensor transitions

## Data Sources

- Patient records: `PatientData.xlsx`
- Pollution records: OpenAQ v3 via `AQI_Data_Collection.py`
- AQI output: `Ahmedabad_AQI_Daily.csv`
- Merged output: `Analysis_Ready_Dataset.csv`

## Core Scripts

- `AQI_Data_Collection.py` - fetch AQI daily data
- `qc_patient_data.py` - validate patient data quality
- `prepare_analysis_dataset.py` - merge + feature engineering
- `expand_patient_data.py` - patient data expansion utility
- `visualize_update.py` - status visualization

## Current Status

- End-to-end data pipeline exists and runs
- Analysis-ready dataset already generated
- Main bottleneck: acquiring sufficient patient records and class balance

## Sample Size Targets

- Preferred final dataset: 1000-1200 rows
- Respiratory: ~250
- Non-respiratory: ~800-1000

## Key Constraints

- Potential class imbalance if non-respiratory controls are low
- Retrospective design limits causal interpretation
- Data quality and completeness depend on ongoing patient extraction

## Implementation Plan (High-Level)

1. Expand patient data continuously
2. QC and rebuild merged dataset in cycles
3. Train baseline models and compare performance
4. Apply explainability methods
5. Finalize manuscript sections and figures

## Working Protocol

1. Activate venv
2. Run data/QC/merge scripts
3. Validate sample size and class balance
4. Update docs when decisions change

## Archive Policy

- Keep root clean for active files only
- Move one-off/testing/debug assets to:
  - `Research/DONE/scripts_archive/`
  - `Research/DONE/data_backups/`
  - `Research/DONE/notebooks_archive/`
  - `Research/DONE/figures/`

## AI Collaboration Protocol

When starting a new AI session, provide:

- This file (`00_master_context.md`)
- `02_constraints_and_decisions.md`
- `03_implementation_plan.md`
- `06_ai_handoff_context.md`

This ensures continuity across assistants with minimal context loss.
