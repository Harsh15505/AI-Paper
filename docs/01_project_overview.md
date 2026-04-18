# 01 - Project Overview

## Research Goal

Build an explainable machine learning model to estimate/predict pediatric respiratory-related hospital admission risk using ambient air pollution exposure features.

## Final Research Title

**Explainable Machine Learning for Predicting Respiratory-Related Pediatric Hospital Admissions Using Ambient Air Pollution Data: A Retrospective Study from an Urban Indian Hospital**

## Problem Statement

The project links patient admission records to daily pollution metrics (PM2.5, PM10, NO2) and derived lag features. The objective is a clinically interpretable model that supports public-health and hospital planning insights.

## Current Data Status

- AQI dataset prepared for Ahmedabad with daily values and lag features
- Analysis-ready merged dataset exists (`Analysis_Ready_Dataset.csv`)
- Patient dataset is still growing, with emphasis on adding enough non-respiratory controls

## Target Outcome

- Final dataset target: roughly **1000-1200 records**
- Suggested class composition target:
  - Respiratory: ~250
  - Non-respiratory: ~800-1000
- Final deliverables:
  - Trained explainable model
  - Performance metrics
  - Feature importance/explanation outputs
  - Paper draft sections and final manuscript
