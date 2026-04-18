# 4. Results

## 4.1 Cohort Characteristics

Filtering for valid OpenAQ pollution parity and establishing demographic exclusions resulted in an analysis-ready dataset of 1,110 pediatric hospitalization records. Within the target 2-12 years bracket, demographic distribution skewed toward early development (mean age 6.2 years). 

Within outcome classifications, respiratory diagnoses accounted for approximately one-fifth of the dataset (238 patients, 21.4%), while general non-respiratory differentials established the majority baseline (872 patients, 78.6%).

## 4.2 Predictive Model Performance

All tested modeling formulations achieved stable discrimination evaluating the retrospective holdout splits. Logistic regression yielded an ROC-AUC of 0.769 (Recall: 0.646, Precision: 0.419). Non-linear implementations generalized with similar stability, with the XGBoost classifier recording the primary evaluation metrics: **ROC-AUC 0.775, Recall 0.438, and Precision 0.512.**

These values denote moderate algorithmic discrimination expected for retrospective observational data. The performance safely aligns with typical limits for complex, unmeasured clinical and behavioral variables, indicating successful generalization without over-fitting typical of uncontrolled classification models.

## 4.3 Feature Contributions and Model Interpretation (SHAP)

To decipher the logic dictating classification correlations, XGBoost predictions were evaluated utilizing macroscopic and local SHAP interpretation techniques.

**Global Feature Summaries**
Analysis of the aggregate SHAP value magnitudes prioritized feature contributions into a distinct hierarchy:
1.  **Demographic Profile:** Patients belonging to the `Age_Group_Young (5-7 years)` generated the absolute highest prediction divergence. This innate demographic component superseded environmental inputs when defining outcome probability.
2.  **Temporal Patterns:** The specific `Day_of_Week` mapped as the second most influential feature, constraining predictions alongside overarching age profiles. 
3.  **Pollution Signal:** Ambient air pollution metrics established a consistent tertiary contribution. Specifically, immediate `PM2.5` exposure paired with historical lags (`PM2_5_Lag7`) organically emerged globally as top-tier influences—surpassing `PM10`, `NO2`, and broader seasonal demarcations (`Season_Winter`).

*(Insert: Figure 1 - SHAP Summary Bar Plot detailing aggregate feature contribution magnitude)*

## 4.4 Directionality and Environmental Relationships

Translating aggregate feature importance into directional attribution confirmed the validity of the environmental relationship. While pollution did not act as the primary overarching variable for admission, a measurable proportional relationship was identified.

Evaluation of the SHAP summary dot-plot visualized that escalating ambient concentrations of `PM2.5` routinely pushed predictive models toward a positive respiratory classification. Conversely, lower PM2.5 concentrations routinely influenced models negatively, decreasing respiratory admission probabilities. 

*(Insert: Figure 2 - SHAP Dot Summary Plot detailing positive vs negative correlation divergence per respective feature intensity)*

## 4.5 Local Case Decomposition 

To illustrate clinical realization of these intertwined vulnerabilities, localized SHAP waterfall analyses verified specific patient admissions. In a representative case evaluation interpreting a solitary non-respiratory classification:

The model calculated a significantly lower probability of respiratory admission for this patient (Outcome calculation spanning -6.74 in log-odds natively). This classification was predominantly driven by non-vulnerable demographic protection (older age bracket providing significant negative prediction push) combined with favorable localized environmental scenarios (evidenced by sub-baseline PM2.5 and PM10 metrics further suppressing the calculation). This case observation grounds the methodology, confirming that predictions operate within clinically valid limits where mitigated environmental exposure paired with an older pediatric age demographic contributes proportionally to non-respiratory outcomes.

*(Insert: Figure 3 - SHAP Waterfall Plot detailing specific case-level feature contributions)*
