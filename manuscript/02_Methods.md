# 3. Methods

## 3.1 Study Design and Cohort

This investigation was structured as a retrospective observational study analyzing hospital admission data. The study population encompassed pediatric inpatients aged 2 to 12 years admitted to a singular urban hospital in Ahmedabad, India. The targeted extraction window was established spanning February 2025 through January 2026. 

Infants and toddlers under age two were excluded due to competing physiological vulnerabilities (e.g., higher baseline susceptibility to neonatal or purely viral, non-environmental etiologies) that could potentially skew the isolation of the environmental signal.

The primary outcome variable modeled was a binary `Respiratory_Label`, designating whether the patient’s primary admission diagnosis documented a respiratory condition (e.g., Pneumonia, Bronchitis, LRTIs) or a non-respiratory differential (e.g., Acute Gastroenteritis, Viral Fever, Trauma).

## 3.2 Data Sourcing and Integration

**Clinical Data:** De-identified patient records included age, gender, date of admission, and primary diagnostic label.
**Environmental Data:** Daily ambient air quality data was retroactively compiled using the OpenAQ v3 API, drawing from localized sensors situated in Ahmedabad. Target pollutants included PM2.5, PM10, and Nitrogen Dioxide (NO2). 

Datasets were matched deterministically utilizing the admission date. To account for delayed physiological responses to pollution, historical exposure pipelines generated "lagged" variables corresponding to pollution averages 1-day and 7-days prior to the admission event (`PM2_5_Lag1`, `PM2_5_Lag7`, etc.).

## 3.3 Feature Engineering

To facilitate unbiased algorithmic learning and account for temporal confounders, extensive feature engineering transitioned temporal timestamps into clinically evaluable proxies:
*   **Temporal and Seasonal Indicators:** The day of the week, chronological week of the year, month, and localized Indian seasonality classifications (Summer, Monsoon, Post-Monsoon, Winter) were abstracted.
*   **Demographic Categorization:** Age metrics were uniformly processed into sub-brackets to map distinct growth-stage risks (Toddler: 2-4, Young: 5-7, Older: 8-12).
*   **Exclusions:** Records demonstrating critical data unavailability (e.g., lack of corresponding temporal pollution endpoint) or fields demonstrating high systemic missingness capable of compromising training integrity (such as unstandardized patient locality) were uniformly excluded from the prediction matrix.

## 3.4 Predictive Modeling 

To baseline the empirical architecture, predictive analysis was evaluated across three common implementations varying in structural rigidity:
1.  **Logistic Regression** (Baseline traditional linear benchmark)
2.  **Random Forest Classifier** (Initial non-linear ensemble)
3.  **eXtreme Gradient Boosting (XGBoost)** (High-capacity gradient tree boosting)

Continuous numerical features were preprocessed via standard scaling (zero mean, unit variance), while discrete categoricals underwent one-hot encoding. To resolve the inherent class imbalance present within retrospective admission prevalence (majority non-respiratory control), algorithms were enforced with balanced class weighting penalties (`class_weight='balanced'` and `scale_pos_weight`), mitigating minority class suppression without synthetically altering valid underlying exposure clusters (e.g. SMOTE). Models were evaluated on an 80/20 randomly stratified train-test holdout mapping the real-world outcome distribution.

Metrics analyzed included the Area Under the Receiver Operating Characteristic Curve (ROC-AUC), F1-Score, sensitivity (recall), and precision.

## 3.5 Interpretability Architecture (SHAP)

Following evaluation, the highest-performing tree-based model natively integrated a TreeExplainer utilizing the SHAP (SHapley Additive exPlanations) paradigm. Based on cooperative game theory, SHAP attributes marginal impact values iteratively for every feature against every prediction constraint. These aggregated Shapley values empowered both global macro-evaluations (identifying overarching feature hierarchies natively driving the dataset predictions) and local micro-evaluations (generating distinct patient-by-patient waterfall decompositions explaining exact contributing risks driving individual admissions).
