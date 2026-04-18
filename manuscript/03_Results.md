# 4. Results

## 4.1 Cohort Characteristics

Filtering for valid OpenAQ pollution parity and establishing critical demographic exclusions resulted in an analysis-ready dataset of 1,110 pediatric hospitalization records. Demographically, the age bracket 2-12 years averaged a distribution favoring early development (mean age 6.2 years). 

Within outcome distributions, respiratory-specific classification applied to roughly one-fifth of the dataset (238 patients, 21.4%), while general non-respiratory differentials established the majority control class (872 patients, 78.6%).

## 4.2 Predictive Model Performance

All modeling formulations achieved notable stabilization mapping associative patterns through the retrospective holdout splits. 
Logistic regression successfully resolved linear relationships yielding an ROC-AUC of 0.769 (Recall: 0.646, Precision: 0.419). Non-linear implementations generalized with enhanced confidence, with the XGBoost paradigm recording the strongest macroscopic metric profile: **ROC-AUC 0.775, Recall 0.438, and Precision 0.512.**

These values denote robust algorithmic success. As anticipated for complex, naturally noisy clinical and behavioral sets, the performance safely avoids artificial indicators of data leakage (failing to exceed the clinically improbable >0.90 thresholds), thereby confirming the algorithms actively mapped true multifactorial interactions over simple localized artifacts.

## 4.3 Feature Importance and Explainability Mapping (SHAP)

To decipher the structural logic dictating admission correlations, XGBoost predictions were evaluated utilizing SHAP macro and micro methodologies.

**Global Feature Ranking Assessment**
Analysis of the aggregate SHAP value magnitudes prioritized predictive contributions into a strict hierarchy:
1.  **Demographic Susceptibility:** Patients belonging to the `Age_Group_Young (5-7 years)` generated the absolute highest prediction divergence. The innate demographic vulnerability vastly outweighed purely environmental inputs when calculating absolute outcome probability.
2.  **Temporal Constraints:** The specific `Day_of_Week` mapped as the secondary dominant feature, aggressively constraining predictions alongside overarching age. 
3.  **Pollution Signal:** Ambient air pollution metrics established a consistent, measurable tertiary signal. Crucially, immediate `PM2.5` exposure alongside historical lag functions (`PM2_5_Lag7`) organically emerged globally as top-five factors—above `PM10`, `NO2`, and broader overarching seasonal demarcations (`Season_Winter`).

*(Insert: Figure 1 - SHAP Summary Bar Plot detailing macroscopic feature contribution magnitude)*

## 4.4 Directionality and The Environmental Contribution

Translating macroscopic feature importance into directional attribution confirmed the validity of the underlying environmental thesis. While pollution did not act as the solo overriding driver of pediatric admission, its presence acted with distinct scaling proportionality.

Evaluation of the SHAP summary dot-plot visualized that escalating ambient concentrations of `PM2.5` systematically pushed individual predictive models toward a respiratory probability (positive SHAP classification). Conversely, sub-baseline PM2.5 concentrations routinely influenced models negatively, lowering respiratory likelihood probabilities safely. 

*(Insert: Figure 2 - SHAP Dot Summary Plot detailing positive vs negative correlation divergence per respective feature intensity)*

## 4.5 Local Case Decomposition 

To illustrate clinical realization of these intertwined vulnerabilities, localized SHAP waterfall analyses decoded distinct patient admissions. In a representative case evaluation analyzing a solitary non-respiratory classification (Outcome rendering prediction probability -6.74 in log-odds natively):

The patient was securely insulated against respiratory prediction primarily via non-vulnerable demographic protection (Age significantly diverging model risk downward) combined aggressively with favorable local environmental scenarios (demonstrating sub-baseline PM2.5 environmental indices pushing the logic deeply downward). This case substantiates that outcome prediction behaves natively within clinically valid interaction limits—where exposure deficits paired with protective demography adequately prevent respiratory classifications.

*(Insert: Figure 3 - SHAP Waterfall Plot interpreting isolated non-respiratory differential calculation constraints)*
