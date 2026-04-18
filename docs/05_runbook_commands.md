# 05 - Runbook Commands

## Activate Environment (PowerShell)

```powershell
(Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned) ; (& ".\\.venv\\Scripts\\Activate.ps1")
```

## Typical Execution Order

```powershell
python AQI_Data_Collection.py
python qc_patient_data.py
python prepare_analysis_dataset.py
python visualize_update.py
```

## Validation Checks

- Confirm `Analysis_Ready_Dataset.csv` updated timestamp changed
- Verify sample size increased as expected
- Verify class balance snapshot (respiratory vs non-respiratory)
- Verify no obvious null spikes in key features

## When New Patient Batch Arrives

1. Update `PatientData.xlsx`
2. Run QC script
3. Rebuild merged dataset
4. Re-check constraints:
   - age 2-12
   - admission date in Feb 2025-Jan 2026
5. Update notes in docs if assumptions changed

## Troubleshooting Notes

- If temporary file `~$PatientData.xlsx` appears, Excel currently has workbook lock
- If AQI pulls look stale/flat, verify correct sensor IDs and v3 endpoint usage
