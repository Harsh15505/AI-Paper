# 02 - Constraints and Locked Decisions

## Locked Study Limits

- Age range: **2-12 years**
- Study period: **February 2025 to January 2026**

## Why the Date Window Is Locked

OpenAQ Ahmedabad data has a practical availability gap before Feb 2025 in the selected station/sensor configuration due sensor/network changes. Usable continuous pollution data begins around Feb 2025 for the selected sensors.

## AQI Source Constraints

- API version: OpenAQ v3
- Endpoint pattern uses sensor-specific daily aggregation
- Correct sensor IDs are required (older duplicate sensors can return stale/historical values)

## Data Quality Constraints

- Current dataset has class imbalance risk (too many respiratory cases relative to controls)
- Need higher non-respiratory count for stable model training and fair evaluation
- Seasonal coverage improves as more patient records are added across months

## Methodological Constraints

- Retrospective observational design (no intervention)
- Admission-date alignment with daily AQI features
- Limited causal claims; focus on predictive and associative insights

## Practical Constraints

- Manual/partial patient data extraction takes time
- Some files (temporary Excel lock files) may appear while workbook is open
- Reproducibility depends on preserving final sensor IDs and preprocessing logic
