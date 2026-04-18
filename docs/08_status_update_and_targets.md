# 08 - Status Update and Targets

## Scope Change Summary

### Previous Design

- Age range: 5-12
- Study period: Dec 2024 to Jan 2026
- Usable sample from initial batch: 6 of 43

### Current Design (Locked)

- Age range: 2-12
- Study period: Feb 2025 to Jan 2026
- Usable sample from initial batch: 17 of 43
- Practical gain: about 3x over previous design

## Current Data Reality

- Existing small batch remains class-imbalanced (respiratory-heavy).
- Priority is to add non-respiratory controls.
- Seasonal breadth improves as additional months are added.

## Target Dataset Profile (Final)

- Total rows: 1000-1200
- Respiratory: about 250-280
- Non-respiratory: about 800-1000
- Age range retained: 2-12
- Date window retained: Feb 2025 to Jan 2026

## Pipeline Changes Already Implemented

- `prepare_analysis_dataset.py` updated for min age = 2
- Age-group feature added (2-4, 5-7, 8-12)
- Merged analysis output regenerated in `Analysis_Ready_Dataset.csv`

## Immediate Next Actions

1. Continue extracting patient records in locked age/date scope.
2. Prioritize non-respiratory cases to improve class balance.
3. Run quality checks and rebuild merged dataset each batch.
4. Keep methods/protocol text aligned with locked decisions.

## Operational Warnings

- Do not request Dec 2024 AQI for this pipeline scope.
- Do not manually merge tables outside the scripts.
- Do not train without including age as predictor.
