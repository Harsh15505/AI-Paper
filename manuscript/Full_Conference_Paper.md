# Evaluating the Association Between Ambient Air Pollution and Pediatric Respiratory Admissions Using Explainable Machine Learning: A Retrospective Study

**Keywords:** Air Pollution, Pediatric Respiratory Disease, Explainable AI, Machine Learning, SHAP, Public Health, Ablation Study

---

## 1. Abstract

**Background:** Amid rapid urbanization, air pollution is identified as one of the exacerbating factors causing respiratory diseases in children. However, in the retrospective observational study it’s challenging to differentiate the influence of the environment in isolation from all other interfering variables, such as demographic factors and temporal patterns of seeking healthcare.
**Objective:** To develop an explainable ML model that will analyze the cases of respiratory hospitalizations of children and determine the contribution made by air pollution, temporality, and demographic factors to the process.
**Methods:** The study adopted the method of analyzing the medical records retrospectively from patients aged between 2-12 years who were admitted in the urban hospital in Ahmedabad, India, from February 2025 to January 2026 (N=1110). Data on air pollution exposures were gathered in daily observations recorded by OpenAQ sensors and included PM2.5, PM10, and NO2. The XGBoost classification algorithm was developed and analyzed via SHapley Additive exPlanations (SHAP).
**Results:** The dataset consisted of 21.4% respiratory hospitalizations, while the remaining 78.6% were non-respiratory. Stability was achieved in evaluation criteria for the base XGBoost algorithm (AUC-ROC = 0.775, Recall = 0.438). Additionally, the SHAP-based feature importance revealed that predictors that had the largest impact on the results corresponded to demographic vulnerability (the age group of 5-7 years) and time features (the day of hospitalization). Thus, excluding these predictors from analysis caused a decline in AUC-ROC value to 0.509, which means that pollution predictors alone cannot contribute to predictions in terms of any other characteristics of the data sample. However, a moderate correlation between pollution predictors and respiratory diseases was found to exist, namely between PM2.5 values and lags.
**Conclusion:** There are several different reasons why hospitalization in relation to respiratory diseases occurs, such as environmental pollution, demographic susceptibility, and evolution in the provision of healthcare services. Environmental pollution plays a moderate role in causing respiratory morbidity among children, which is facilitated by behavioral risk factors.

---

## 2. Introduction
There is considerable pressure on urban healthcare facilities due to the respiratory diseases affecting children. The physiological underdevelopment of immune systems in pediatric patients makes them more susceptible to the ill effects of air pollution. Thus, decoding these interacting factors is critical for dynamic pediatric healthcare resource planning within the context of rapidly urbanizing Indian cities.

Previous studies have documented the causal associations between coarse particulate matter (PM2.5, PM10) and severe respiratory admissions. However, separating the impact of environmental factors from behavioral, temporal, and demographic variables remains a difficult task in clinical settings. Health-seeking behavior, such as the patient delay effect favoring weekday visits, along with the inherent differences in age-related biological sensitivity, can impede the isolation of the true environmental effect.

Linear models are typically insufficient in dealing with the complicated covariates characteristic of clinical studies. Machine learning methods can capture complex interactions for classification. Nonetheless, in order to maintain clinical relevance, XAI approaches need to be incorporated into AI development projects.

The current study employs the concept of explainable artificial intelligence models to examine observational pediatric respiratory admission cases based on real-world retrospective hospital data as well as localized sensor endpoints. The approach does not involve developing a prospective clinical early warning tool but, rather, uses an XGBoost classifier to model the non-linear interactions between environmental exposure, demographics, and hospital admissions. The study applies the SHAP method alongside the ablation technique to quantify feature contributions.

---

## 3. Related Work

The application of machine learning to environmental health has transitioned from conventional linear regression to high-capacity non-linear modeling. Early epidemiological frameworks predominantly utilized autoregressive integrated moving average (ARIMA) or generalized additive models (GAMs) to map respiratory outcomes against PM2.5 spikes. While effective at defining macroscopic correlations, these methods inherently struggled to natively process non-linear interactions between demographic vulnerabilities and staggered temporal healthcare utilization.

Subsequent literature has therefore focused on tree-based classification systems known as Random Forests and Gradient Boosted Models (GBMs). Studies such as Brokamp et al. and Zheng et al. demonstrate strong connections regarding patients with respiratory vulnerabilities and the presence of particulate matter resulting in acute readmissions. Yet pediatric subjects pose a new challenge as they possess a high amount of variability due to development from birth through pre-adolescent years.

Additionally, typical machine learning models tends to function like a "black box" as it can provide reliable predictive metrics but lacks clinical insight as the results remain opaque. In particular, Shapley Additive Explanations (SHAP), based on the concept of cooperative games, provides local explanation exactness for each individual patient over traditional XGBoost probability matrices. The current research combines XGBoost and SHAP within a localized Indian pediatric sample to explicitly implement a feature ablation technique targeting the documented healthcare weekend delay effect.

---

## 4. Methods

### 4.1 Study Design and Cohort EDA
This retrospective observational study was conducted between February 2025 and January 2026. The population comprised hospitalized children between 2 to 12 years old. The study did not include infants younger than 2 years old because of their physiological susceptibility to other factors (newborns and purely viral diseases). Based on demographic criteria, the validated target population (N=1,110) included 238 respiratory diagnoses (21.4%) and 872 non-respiratory diagnoses (78.6%).

*Table 1. Baseline Characteristics (N=1,110)*

| Metric | Overall | Respiratory (n=238) | Non-Respiratory (n=872) |
| :--- | :--- | :--- | :--- |
| Mean Age (Years) | 6.2 ± 3.0 | 4.0 ± 2.5 | 6.7 ± 2.9 |
| Gender (% Male) | 72.4% | 74.8% | 71.8% |
| Mean PM2.5 (µg/m³) | 36.5 | 39.2 | 35.8 |
| Mean PM10 (µg/m³) | 95.2 | 95.0 | 95.2 |

Baseline demographic statistics illustrated a targeted divergence in age (respiratory admissions concentrated generally toward early development, ~4.0 years) and an associative inflation in PM2.5 concentrations corresponding directly with respiratory classifications.

### 4.2 Data Sourcing and Feature Engineering
Retroactive ambient air quality data were collected via the OpenAQ API with regards to Ahmedabad sensor data. Historical exposures were constructed through computation of lag variables with respect to 1-day lag average (PM2.5_Lag1) and 7-day lag average (PM2.5_Lag7). Timestamps were standardized as Day_of_Week, Month, and Season, while age information was categorized into Toddler, Young, and Older.

### 4.3 Algorithmic Execution and Mathematical Foundation 
The XGBoost model was chosen as the most effective non-linear algorithm due to its ability to deal effectively with sparse, tabular data as well as inherent L1/L2 regularization to prevent noise overfitting. An 80/20 random stratified train/test split was utilized by the models, which incorporated a weight based on positive scaling of the occurrences.

SHAP TreeExplainer mapped resultant probability outcomes. SHAP calculates the marginal contribution of a feature across all viable feature permutations using an additive framework metric yielding strict theoretical guarantees missing in baseline algorithmic feature-importance charts. (e.g., consistency and missingness). 

### 4.4 Ablation Study Protocol
To isolate systemic confounding variables, a secondary ablation experiment was conducted. An alternative modeling split forcefully removed all chronological, behavioral (Day_of_Week, Month), and individual demographic vectors (Age_Years, Age_Group) isolating the predictive environment exclusively to raw ambient pollution vectors. Evaluating the magnitude of metric collapse provides empirical evidence for establishing primary interaction drivers.

---

## 5. Results

### 5.1 Baseline Predictive Model Performance
The first version of the XGBoost model led to an **AUC of 0.775, a Recall of 0.438, and a Precision of 0.512.** This shows that the desired learning capabilities required to cope with the assessment of the environment in real life with the potential presence of noise are available, and the dependence on data leakage correlations is minimal. Furthermore, the comparative analysis indicated that the regular version of the Logistic Regression algorithm (AUC of 0.769) operated at least non-linearly like the first one.

### 5.2 Ablation Findings Confirm Primary Dependencies
Nevertheless, the feature-ablated variant of XGBoost, where the environmental proxies and matrix features were utilized, delivered poor performance metrics: an **ROC-AUC of 0.509** (which means no better than randomness), and very low Recall metric of 0.333.

Consequently, such metrics indicate that pollution variables provide a measurable but secondary predictive signal, and are insufficient to accurately classify admissions in isolation without interacting with behavioral or demographic catalysts. Furthermore, they point to the conclusion that hospitalization takes place because of the interplay between demography and personal behavior factors. 

### 5.3 Feature Contributions and Relationships (SHAP)
The SHAP analysis of the baseline classifier showed that demographics (age) and temporal (day of the week) variables drive the predictive abilities of the models:

- **Demographic Variables:** Age was the main determinant that caused large differences in probabilities, making up the first predictor variable.
- **Time Factors:** Day of the week constituted the second predictor, capturing health care service usage patterns instead of demographic variables.
- **Environment:** Daily levels of PM2.5 as well as their lagged 7-day version always exhibited an associated correlation controlling marginal rises in classification probabilities.

---

## 6. Discussion and Policy Implications

### 6.1 Synthesizing Biological Patterns vs Behavior
This retrospective framework successfully delineated ambient air pollution interactions against complex clinical medicine realities. Interpreting SHAP contributions highlights that while PM2.5 acts as a persistent independent environmental stressor, it exclusively operates as a secondary aggravating layer upon extreme demographic baselines.

The profound hierarchical presence of `Day_of_Week` alongside the ablation study confirmation explicitly emphasizes systemic healthcare utilization behavior over strict immediate biological causative risks. Pediatric admissions suffer from "weekend effect" delays—where guardians routinely defer specialized evaluations to standard operational weekdays. The resultant peak algorithmically learns the healthcare ecosystem's socio-economic pacing simultaneously alongside patient disease metrics. Acknowledging behavioral artifacts correctly characterizes why generic forecasting mechanisms repeatedly fail without rigid observational tuning.

### 6.2 Clinical and Public Health Implications
Functionally translating this algorithmic associative behavior yields actionable insights for urban Indian hospital infrastructure:
*   **Predictive Staffing Realities:** Because pollution operates via `Lag7` exposure delays paired extensively behind generic day-of-week healthcare utilization, administrators can track regional PM2.5 spikes anticipating resource influxes manifesting exclusively on subsequent Mondays or Tuesdays, rather than immediately matching real-time air quality indexing.
*   **Targeted Vulnerability Tracking:** Preventative community action can be mathematically prioritized primarily toward the hyper-susceptible pre-adolescent block identified exclusively via SHAP logic over generic pediatric broadcast warnings.

### 6.3 Limitations
Due to retrospective structuring, this framework interprets associative risk probabilities, severely limited inherently from defining strict deterministic biological causality. Aggregated OpenAQ datasets introduce single monitoring station bias, creating a limitation by assuming uniform spatial exposure across the city while omitting localized micro-exposures or indoor environments. Furthermore, the dataset omits unmeasured patient comorbidities (asthma staging) shaping internal baseline resistance. 

---

## 7. Conclusion

This execution of explainable machine learning evaluated the complex factors influencing pediatric respiratory admissions. We established realistically balanced parameters confirming that respiratory hospitalizations emerge from chronological intersections between fundamental demographic susceptibility and behavioral healthcare utilization. While ambient PM2.5 exposures independently associate sequentially with elevated respiratory manifestations, ablation experimentation confirms they perform solely as secondary environmental aggravators functioning within demographic contexts. Defining explicitly non-deterministic associative interpretations affords clinicians reliable public-health lenses free from prospective forecasting inaccuracies defining modern ambient epidemiological morbidity.
