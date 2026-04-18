# AI Research Paper - Project Docs Hub

This folder contains the full working context for the project so multiple AI assistants can continue work consistently.

## Quick Start

1. Read `01_project_overview.md`
2. Read `02_constraints_and_decisions.md`
3. Read `03_implementation_plan.md`
4. Use `06_ai_handoff_context.md` before assigning tasks to another AI
5. Read `07_methodology_age_range_justification.md` for methods wording
6. Read `08_status_update_and_targets.md` for latest targets

## Contents

- `00_master_context.md`: Single-file complete project context
- `01_project_overview.md`: Research summary and objective
- `02_constraints_and_decisions.md`: Locked decisions and constraints
- `03_implementation_plan.md`: Phase-by-phase execution plan
- `04_data_pipeline_and_files.md`: Data flow and file map
- `05_runbook_commands.md`: Command sequence and operational checks
- `06_ai_handoff_context.md`: Copy-paste AI context block
- `07_methodology_age_range_justification.md`: Methods-ready age rationale
- `08_status_update_and_targets.md`: Scope-change summary and final targets

## Key Project Identity

- Final Title:
  - **Explainable Machine Learning for Predicting Respiratory-Related Pediatric Hospital Admissions Using Ambient Air Pollution Data: A Retrospective Study from an Urban Indian Hospital**
- Study Population:
  - Pediatric inpatients, age **2-12 years**
- Study Period:
  - **February 2025 to January 2026**
- Current Limitation:
  - OpenAQ Ahmedabad data gap before Feb 2025 due network/sensor changes

## Active Core Files (root)

- `AQI_Data_Collection.py`
- `prepare_analysis_dataset.py`
- `expand_patient_data.py`
- `qc_patient_data.py`
- `visualize_update.py`
- `Ahmedabad_AQI_Daily.csv`
- `Analysis_Ready_Dataset.csv`
- `PatientData.xlsx`

## Archived/Reference Material

- `Research/DONE/scripts_archive/` (old debugging/exploration scripts)
- `Research/DONE/data_backups/` (backup Excel files)
- `Research/DONE/notebooks_archive/` (temporary notebooks)
- `Research/DONE/figures/` (generated figures)
