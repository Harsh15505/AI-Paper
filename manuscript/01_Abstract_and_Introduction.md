# Evaluating the Association Between Ambient Air Pollution and Pediatric Respiratory Admissions Using Explainable Machine Learning: A Retrospective Study

## 1. Abstract

**Background:** Ambient air pollution is a recognized exacerbating factor for pediatric respiratory conditions, particularly in rapidly urbanizing environments. However, isolating the environmental signal from confounding variables, such as demographic susceptibility and temporal healthcare utilization behavior, remains challenging in retrospective clinical studies.
**Objective:** To develop an explainable machine learning framework to evaluate pediatric respiratory hospital admissions and map the relative contributions of air pollution, temporal metrics, and demographic characteristics.
**Methods:** We conducted a retrospective observational study on pediatric inpatients (aged 2-12 years) admitted to an urban hospital in Ahmedabad, India, between February 2025 and January 2026. Patient records were integrated with daily ambient pollution exposure metrics (PM2.5, PM10, NO2). A suite of baseline classification models was trained, with the strongest model interpreted using SHapley Additive exPlanations (SHAP) to decode structural feature contributions.
**Results:** The dataset comprised 1,110 records (21.4% respiratory, 78.6% non-respiratory). An XGBoost classifier demonstrated stable evaluation metrics (ROC-AUC 0.775, Recall 0.438). SHAP analysis revealed that demographic susceptibility (specifically the 5-7 year age bracket) and temporal patterns (day incident to admission) provided the dominant contributions to classification. Air pollution—specifically PM2.5 and its lagged exposures—demonstrated a consistent, secondary relationship with clear directionality proportional to exposure magnitude.
**Conclusion:** Respiratory admissions emerge from a complex combination of environmental exposure, demographic susceptibility, and temporal healthcare patterns. Ambient air pollution demonstrates a moderate, independent contribution, highlighting its persistent role as an exacerbator of pediatric respiratory morbidity alongside overarching behavioral and demographic variables.

**Keywords:** Air Pollution, Pediatric Respiratory Disease, Explainable AI, Machine Learning, SHAP, Public Health

---

## 2. Introduction

Pediatric respiratory conditions place immense strain on urban healthcare infrastructure, particularly in rapidly developing regions like Ahmedabad, India. Given the physiological immaturity of respiratory immune defenses, young children are uniquely vulnerable to the adverse effects of ambient air pollution, making environmental exposure a critical focal point in public health analytics. 

While relationships between particulate matter (e.g., PM2.5, PM10) and respiratory hospitalizations are documented in epidemiological literature, parsing the direct contribution of pollution against confounding behavioral, temporal, and demographic realities is a persistent challenge in retrospective clinical reporting. Healthcare utilization behavior—such as patient-delay phenomena prioritizing weekday over weekend care—alongside inherently varying age-based susceptibilities actively obscure the environmental signal.

Traditional linear techniques often struggle to untangle the non-linear interactions these variables exhibit. Machine learning offers an alternative capable of handling multi-dimensional covariates. To preserve clinical interpretability, this dynamic has increasingly driven researchers toward explainable AI (XAI) paradigms, which explicitly bridge algorithmic output with clinical meaning.

This study implements an explainable machine learning architecture to evaluate pediatric respiratory admissions using real-world retrospective hospital data paired with localized OpenAQ sensor endpoints. Rather than constructing a prospective forecasting tool, this approach utilizes classification methodologies mathematically as an engine to tease apart non-linear associations. Utilizing SHAP (SHapley Additive exPlanations), we map the structural hierarchy of admissions—evaluating the relationship between ambient air pollution, intense demographic susceptibilities, and temporal healthcare behavior.
