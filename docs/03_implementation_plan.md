# 03 - Implementation Plan

## Phase 1 - Data Finalization

1. Continue expanding `PatientData.xlsx`
2. Ensure inclusion criteria are enforced:
   - Age 2-12
   - Admission date in Feb 2025-Jan 2026
3. Run QC with `qc_patient_data.py`
4. Generate/refresh merged dataset with `prepare_analysis_dataset.py`

### Exit Criteria

- Near-target sample size (ideally 1000+)
- Better class balance
- No critical missing fields in modeling columns

## Phase 2 - Feature and Split Strategy

1. Confirm feature set from pollution and metadata columns
2. Define train/validation/test split strategy
3. Apply class balancing strategy if needed (weights/resampling)
4. Freeze preprocessing for reproducibility

### Exit Criteria

- Stable feature matrix and label vector
- Documented preprocessing and split logic

## Phase 3 - Modeling and Explainability

1. Train baseline models (e.g., logistic regression, tree-based)
2. Compare performance (AUC, F1, recall, precision, calibration as needed)
3. Generate explainability outputs (global + local)
4. Stress-test model robustness

### Exit Criteria

- Selected final model with documented reasons
- Explainability outputs ready for paper figures/tables

## Phase 4 - Paper Writing and Packaging

1. Methods section finalization
2. Results tables/figures
3. Discussion, limitations, and ethics framing
4. Final proofreading and formatting

### Exit Criteria

- Submission-ready manuscript with reproducible appendix/code notes

## Weekly Operational Loop (while data arrives)

1. Add new patient records
2. Run QC
3. Rebuild merged dataset
4. Update sample-size and class-balance snapshot
5. Log changes in docs if assumptions shift
