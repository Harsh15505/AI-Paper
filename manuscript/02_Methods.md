# 3. Methods

## 3.1 Study Design and Cohort

This investigation was structured as a retrospective observational study analyzing hospital admission data. The study population encompassed pediatric inpatients aged 2 to 12 years admitted to a singular urban hospital in Ahmedabad, India. The targeted extraction window was established spanning February 2025 through January 2026. 

Infants and toddlers under age two were excluded due to competing physiological vulnerabilities (e.g., higher baseline susceptibility to neonatal or purely viral, non-environmental etiologies) that could potentially skew the environmental analysis.

The primary outcome was designated by a binary `Respiratory_Label`, classifying whether the patient’s primary admission diagnosis documented a respiratory condition (e.g., Pneumonia, Bronchitis, LRTIs) or a non-respiratory differential (e.g., Acute Gastroenteritis, Viral Fever, Trauma).

## 3.2 Data Sourcing and Integration

**Clinical Data:** De-identified patient records included age, gender, date of admission, and primary diagnostic label.
**Environmental Data:** Daily ambient air quality data was retroactively compiled using the OpenAQ v3 API, drawing from localized sensors situated in Ahmedabad. Target pollutants included PM2.5, PM10, and Nitrogen Dioxide (NO2). 

Datasets were matched deterministically leveraging the admission date. To account for delayed physiological responses to pollution, historical exposure pipelines generated "lagged" variables corresponding to pollution averages 1-day and 7-days prior to the admission event (`PM2_5_Lag1`, `PM2_5_Lag7`, etc.).

## 3.3 Feature Engineering

To facilitate algorithmic processing and account for temporal confounders, timestamps were transformed into standardized temporal proxies:
*   **Temporal and Seasonal Indicators:** The day of the week, chronological week of the year, month, and localized Indian seasonality classifications (Summer, Monsoon, Post-Monsoon, Winter).
*   **Demographic Categorization:** Age metrics were processed into sub-brackets (Toddler: 2-4, Young: 5-7, Older: 8-12).
*   **Exclusions:** Records lacking corresponding temporal pollution endpoints or demonstrating significant systemic missingness (e.g., unstandardized patient locality) were excluded prior to analysis.

## 3.4 Modeling Approach

The dataset was evaluated using three standardized classification algorithms: Logistic Regression, Random Forest, and eXtreme Gradient Boosting (XGBoost). Continuous numerical features were scaled symmetrically (StandardScaler), while categorical variables underwent one-hot encoding. To account for class imbalance, algorithms applied balanced class weighting penalties (`class_weight='balanced'` and `scale_pos_weight`). Models were evaluated on an 80/20 randomly stratified train-test holdout mapping the real-world outcome distribution.

Metrics analyzed included the Area Under the Receiver Operating Characteristic Curve (ROC-AUC), F1-Score, sensitivity (recall), and precision.

## 3.5 Model Interpretation (SHAP)

Following evaluation, the highest-performing tree-based model was analyzed using SHAP (SHapley Additive exPlanations) to interpret feature contributions. SHAP attributes marginal impact values for every feature. These values empowered both global interpretations (identifying aggregate feature prominence defining the dataset) and local evaluation (generating specific waterfall decompositions illustrating feature contributions mapping to an individual patient classification).
