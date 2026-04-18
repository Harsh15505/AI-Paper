# Appendix A: Reproducibility and Methods Details

## A.1 Compute Environment
All data preprocessing, modeling, and interpretation implementations natively executed in Python (`v3.12.2`). Core libraries utilized span `pandas` (v3.0.2) and `numpy` (v2.4.4) for data structures, `scikit-learn` (v1.6.1) spanning macroscopic pipeline implementation and scaler transformations, and `xgboost` (v2.1.4) alongside `shap` (v0.46.0) corresponding to the primary interpretative architecture. Visualizations natively compiled utilizing `matplotlib` and `seaborn`.

## A.2 Dataset Parity Constraints
Target admission records missing either core internal fields (`Age_Years`, `Admission_Date`, `Respiratory_Label`) or existing beyond boundary dates defined strictly by verifiable sensor endpoints mapping to the OpenAQ repository (yielding PM2.5 configurations exclusively valid after February 24, 2025) were dropped strictly during dataset instantiation.

## A.3 Hyperparameter Schemas and Weighting
All models natively incorporated pseudo-random seed constants (`random_state=42`) ensuring replicable iterations. No grid search optimization functions were strictly applied in lieu of deploying generalized baseline structures preventing overfit bias traps. To adjust macroscopic class imbalance, baseline algorithms inherently mapped proportionate outcome penalties (applying `class_weight='balanced'` uniformly across standard regression and random forest arrays, substituting equivalent `scale_pos_weight` ratios dynamically to XGBoost structures proportionally equating binary counts internally).

## A.4 Feature Preprocessor
Categorical derivations corresponding to (`Gender`, `Season`, `Age_Group`, `Quarter`) underwent explicit One-Hot Encoding dropping isolated first-reference classes implicitly resolving multi-collinearity constraints. Continuous numerical equivalents (Age explicitly, macroscopic PM variants, and relative temporal days) scaled symmetrically bounding mean and unit variation parameters via `StandardScaler`. Patient `Locality` string identifiers inherently yielding ~32% internal systemic missingness and lacking uniformity norms were explicitly removed completely to enforce generalized robustness across non-stratified validation splits.
