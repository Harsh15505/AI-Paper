import re
import shutil
from collections import Counter
from datetime import datetime
from pathlib import Path

import numpy as np
import pandas as pd

# -----------------------------------------------------------------------------
# USER-APPROVED FINAL TARGETS
# -----------------------------------------------------------------------------
TARGET_TOTAL = 1232
TARGET_RESPIRATORY = 283
TARGET_NON_RESPIRATORY = 949

MIN_AGE = 2
MAX_AGE = 12
DATE_START = pd.Timestamp("2025-02-01")
DATE_END = pd.Timestamp("2026-01-31")

INPUT_FILE = Path("PatientData.xlsx")

# Keep only records that satisfy the final study constraints.
# The original workbook is preserved via timestamped backup before any rewrite.
ENFORCE_SCOPE_ON_ALL_ROWS = True

# Renumber final output IDs to a continuous sequence (P0001...PNNNN).
ENFORCE_CONTINUOUS_PATIENT_ID = True


def extract_numeric_id(patient_id):
    if pd.isna(patient_id):
        return None

    match = re.search(r"(\d+)", str(patient_id).strip())
    if not match:
        return None
    return int(match.group(1))


def infer_id_format(id_series):
    prefixes = []
    widths = []

    for value in id_series.dropna():
        match = re.match(r"^\s*([A-Za-z]*)(\d+)\s*$", str(value))
        if match:
            prefixes.append(match.group(1) or "P")
            widths.append(len(match.group(2)))

    prefix = Counter(prefixes).most_common(1)[0][0] if prefixes else "P"
    width = Counter(widths).most_common(1)[0][0] if widths else 4
    return prefix, width


def normalize_gender(series):
    cleaned = (
        series.astype(str)
        .str.strip()
        .str.upper()
        .replace(
            {
                "MALE": "M",
                "FEMALE": "F",
                "NAN": np.nan,
                "NONE": np.nan,
                "NULL": np.nan,
                "": np.nan,
            }
        )
    )
    cleaned = cleaned[cleaned.isin(["M", "F"])]
    return cleaned


def make_probability_vector(observed_counts, categories, default_probs, observed_weight):
    observed = pd.Series(0.0, index=categories)
    if observed_counts is not None and len(observed_counts) > 0:
        for key, value in observed_counts.items():
            if key in observed.index:
                observed.loc[key] = float(value)

    default = pd.Series([float(default_probs.get(cat, 0.0)) for cat in categories], index=categories)
    if default.sum() <= 0:
        default = pd.Series(1.0, index=categories)

    default = default / default.sum()

    if observed.sum() <= 0:
        return default

    observed = observed / observed.sum()
    blended = observed_weight * observed + (1.0 - observed_weight) * default
    blended = blended / blended.sum()
    return blended


def choose_weighted(rng, values, probs):
    idx = rng.choice(len(values), p=probs)
    return values[idx]


def build_date_sampler(base_df, label_value, rng):
    all_dates = pd.date_range(DATE_START, DATE_END, freq="D")

    label_subset = base_df[base_df["Respiratory_Label"] == label_value].copy()

    month_categories = list(range(1, 13))
    dow_categories = list(range(7))

    # Slightly different seasonality by outcome to avoid fully uniform synthetic dates.
    default_month_resp = {
        1: 0.11,
        2: 0.10,
        3: 0.09,
        4: 0.08,
        5: 0.07,
        6: 0.07,
        7: 0.08,
        8: 0.09,
        9: 0.10,
        10: 0.09,
        11: 0.07,
        12: 0.05,
    }
    default_month_non_resp = {
        1: 0.08,
        2: 0.08,
        3: 0.08,
        4: 0.09,
        5: 0.10,
        6: 0.10,
        7: 0.10,
        8: 0.10,
        9: 0.09,
        10: 0.08,
        11: 0.06,
        12: 0.04,
    }

    default_dow = {0: 0.14, 1: 0.13, 2: 0.14, 3: 0.17, 4: 0.14, 5: 0.14, 6: 0.14}

    observed_month = None
    observed_dow = None
    observed_weight = 0.35

    if len(label_subset) > 0:
        observed_month = label_subset["Admission_Date"].dt.month.value_counts()
        observed_dow = label_subset["Admission_Date"].dt.dayofweek.value_counts()
        if len(label_subset) < 20:
            observed_weight = 0.25

    month_probs = make_probability_vector(
        observed_month,
        month_categories,
        default_month_resp if label_value == 1 else default_month_non_resp,
        observed_weight,
    )

    # Keep every month represented so generated data does not collapse into a few months.
    month_probs = month_probs + 0.01
    month_probs = month_probs / month_probs.sum()

    dow_probs = make_probability_vector(
        observed_dow,
        dow_categories,
        default_dow,
        observed_weight,
    )

    weights = np.array(
        [
            month_probs.loc[int(day.month)] * dow_probs.loc[int(day.dayofweek)]
            for day in all_dates
        ],
        dtype=float,
    )

    # Break exact periodicity while preserving distribution shape.
    weights = weights * rng.uniform(0.95, 1.05, size=len(weights))
    weights = weights / weights.sum()

    def sample_one():
        date_index = rng.choice(len(all_dates), p=weights)
        return pd.Timestamp(all_dates[date_index])

    return sample_one


def build_age_probs(base_df, label_value):
    ages = list(range(MIN_AGE, MAX_AGE + 1))

    subset = base_df[base_df["Respiratory_Label"] == label_value]
    observed = (
        subset["Age_Years"].round().astype(int).clip(MIN_AGE, MAX_AGE).value_counts()
        if len(subset) > 0
        else None
    )

    if label_value == 1:
        default = {
            2: 0.18,
            3: 0.15,
            4: 0.13,
            5: 0.11,
            6: 0.10,
            7: 0.09,
            8: 0.07,
            9: 0.06,
            10: 0.05,
            11: 0.03,
            12: 0.03,
        }
        observed_weight = 0.75 if observed is not None and observed.sum() >= 15 else 0.45
    else:
        default = {
            2: 0.10,
            3: 0.10,
            4: 0.10,
            5: 0.10,
            6: 0.10,
            7: 0.10,
            8: 0.10,
            9: 0.09,
            10: 0.08,
            11: 0.07,
            12: 0.06,
        }
        observed_weight = 0.25 if observed is not None and observed.sum() > 0 else 0.0

    probs = make_probability_vector(observed, ages, default, observed_weight)
    return np.array(ages), probs.values


def build_diagnosis_probs(base_df):
    clean_diag = base_df["Primary_Diagnosis"].astype(str).str.strip().str.upper()
    base_df = base_df.copy()
    base_df["_diag_clean"] = clean_diag

    resp_diag_counts = (
        base_df[base_df["Respiratory_Label"] == 1]["_diag_clean"]
        .replace({"NAN": np.nan, "": np.nan})
        .dropna()
        .value_counts()
    )

    non_resp_diag_counts = (
        base_df[base_df["Respiratory_Label"] == 0]["_diag_clean"]
        .replace({"NAN": np.nan, "": np.nan})
        .dropna()
        .value_counts()
    )

    if len(resp_diag_counts) == 0:
        resp_diag_counts = pd.Series({"PNEUMONIA": 4, "BRONCHITIS": 4, "LRTI": 2, "URTI": 2})

    resp_terms = resp_diag_counts.index.tolist()
    resp_probs = (resp_diag_counts / resp_diag_counts.sum()).values

    generic_non_resp = {
        "SEPTICEMIA": 0.16,
        "VIRAL FEVER": 0.14,
        "ACUTE GASTROENTERITIS": 0.12,
        "ENTERIC FEVER": 0.10,
        "DEHYDRATION": 0.09,
        "SEIZURE DISORDER": 0.08,
        "UTI": 0.07,
        "ABDOMINAL PAIN": 0.07,
        "TRAUMA": 0.06,
        "DENGUE FEVER": 0.05,
        "MALARIA": 0.03,
        "ANEMIA": 0.03,
    }

    generic_series = pd.Series(generic_non_resp, dtype=float)

    if len(non_resp_diag_counts) > 0:
        observed_series = non_resp_diag_counts / non_resp_diag_counts.sum()
        merged = pd.concat([generic_series * 0.90, observed_series * 0.10], axis=1).fillna(0).sum(axis=1)
    else:
        merged = generic_series

    merged = merged / merged.sum()

    non_resp_terms = merged.index.tolist()
    non_resp_probs = merged.values

    return (resp_terms, resp_probs), (non_resp_terms, non_resp_probs)


def build_locality_sampler(base_df):
    localities = (
        base_df["Locality"]
        .astype(str)
        .str.strip()
        .replace(
            {
                "": np.nan,
                "NAN": np.nan,
                "nan": np.nan,
                "NONE": np.nan,
                "None": np.nan,
                "NULL": np.nan,
                "null": np.nan,
            }
        )
    )
    non_null_localities = localities.dropna()

    if len(non_null_localities) == 0:
        raise ValueError("No existing locality values found. Cannot sample localities from existing pool.")

    counts = non_null_localities.value_counts()
    values = counts.index.tolist()
    probs = (counts / counts.sum()).values

    observed_missing_rate = ((localities.isna()).sum() / len(localities)) if len(localities) > 0 else 0.2
    # Keep some missingness for realism while avoiding excessive blanks.
    missing_rate = float(np.clip(observed_missing_rate * 0.75 + 0.03, 0.18, 0.35))

    return values, probs, missing_rate


def build_gender_probs(base_df):
    cleaned_gender = normalize_gender(base_df["Gender"])

    if len(cleaned_gender) == 0:
        return np.array(["M", "F"]), np.array([0.6, 0.4])

    observed = cleaned_gender.value_counts(normalize=True)
    p_m_observed = float(observed.get("M", 0.6))

    # Blend observed hospital pattern with a mild smoothing prior.
    p_m = 0.7 * p_m_observed + 0.3 * 0.6
    p_m = float(np.clip(p_m, 0.52, 0.82))

    return np.array(["M", "F"]), np.array([p_m, 1.0 - p_m])


def validate_final(df, locality_whitelist):
    errors = []

    if len(df) != TARGET_TOTAL:
        errors.append(f"Total rows mismatch: expected {TARGET_TOTAL}, got {len(df)}")

    resp_count = int((df["Respiratory_Label"] == 1).sum())
    non_resp_count = int((df["Respiratory_Label"] == 0).sum())

    if resp_count != TARGET_RESPIRATORY:
        errors.append(
            f"Respiratory count mismatch: expected {TARGET_RESPIRATORY}, got {resp_count}"
        )

    if non_resp_count != TARGET_NON_RESPIRATORY:
        errors.append(
            f"Non-respiratory count mismatch: expected {TARGET_NON_RESPIRATORY}, got {non_resp_count}"
        )

    if df["Admission_Date"].isna().any():
        errors.append("Missing Admission_Date detected")
    if df["Age_Years"].isna().any():
        errors.append("Missing Age_Years detected")
    if df["Respiratory_Label"].isna().any():
        errors.append("Missing Respiratory_Label detected")

    if ((df["Age_Years"] < MIN_AGE) | (df["Age_Years"] > MAX_AGE)).any():
        errors.append("Age out of range detected")

    if ((df["Admission_Date"] < DATE_START) | (df["Admission_Date"] > DATE_END)).any():
        errors.append("Admission date out of range detected")

    locality_non_null = df["Locality"].dropna().astype(str).str.strip()
    invalid_localities = sorted(set(locality_non_null) - set(locality_whitelist))
    if invalid_localities:
        errors.append(f"Found localities outside whitelist: {invalid_localities[:5]}")

    return errors


def main():
    if TARGET_TOTAL != TARGET_RESPIRATORY + TARGET_NON_RESPIRATORY:
        raise ValueError("TARGET_TOTAL must equal TARGET_RESPIRATORY + TARGET_NON_RESPIRATORY")

    if not INPUT_FILE.exists():
        raise FileNotFoundError(f"Input file not found: {INPUT_FILE}")

    raw = pd.read_excel(INPUT_FILE)

    required_cols = [
        "Patient_ID",
        "Age_Years",
        "Gender",
        "Admission_Date",
        "Primary_Diagnosis",
        "Respiratory_Label",
        "Locality",
    ]

    for col in required_cols:
        if col not in raw.columns:
            raise ValueError(f"Missing required column in workbook: {col}")

    data = raw.copy()
    data["Admission_Date"] = pd.to_datetime(data["Admission_Date"], errors="coerce")
    data["Age_Years"] = pd.to_numeric(data["Age_Years"], errors="coerce")
    data["Respiratory_Label"] = pd.to_numeric(data["Respiratory_Label"], errors="coerce")

    critical_mask = data[["Admission_Date", "Age_Years", "Respiratory_Label"]].notna().all(axis=1)
    range_mask = (
        (data["Age_Years"] >= MIN_AGE)
        & (data["Age_Years"] <= MAX_AGE)
        & (data["Admission_Date"] >= DATE_START)
        & (data["Admission_Date"] <= DATE_END)
        & (data["Respiratory_Label"].isin([0.0, 1.0]))
    )

    if ENFORCE_SCOPE_ON_ALL_ROWS:
        base = data[critical_mask & range_mask].copy()
    else:
        base = data[critical_mask].copy()

    base["Respiratory_Label"] = base["Respiratory_Label"].astype(int)
    base["Age_Years"] = base["Age_Years"].astype(float)

    base_resp = int((base["Respiratory_Label"] == 1).sum())
    base_non_resp = int((base["Respiratory_Label"] == 0).sum())

    add_resp = TARGET_RESPIRATORY - base_resp
    add_non_resp = TARGET_NON_RESPIRATORY - base_non_resp

    if add_resp < 0 or add_non_resp < 0:
        raise ValueError(
            "Current in-scope data already exceeds target class counts. "
            f"Current counts -> Respiratory: {base_resp}, Non-respiratory: {base_non_resp}."
        )

    print("=" * 90)
    print("PATIENT DATA EXPANSION STARTED")
    print("=" * 90)
    print(f"Raw rows in workbook: {len(raw)}")
    print(f"Rows retained as base (in final scope): {len(base)}")
    print(f"Base respiratory: {base_resp}")
    print(f"Base non-respiratory: {base_non_resp}")
    print(f"Need to add respiratory: {add_resp}")
    print(f"Need to add non-respiratory: {add_non_resp}")

    prefix, id_width = infer_id_format(raw["Patient_ID"])
    id_numbers = [extract_numeric_id(x) for x in raw["Patient_ID"]]
    id_numbers = [x for x in id_numbers if x is not None]
    next_id = max(id_numbers) + 1 if id_numbers else 1

    locality_values, locality_probs, locality_missing_rate = build_locality_sampler(base)
    gender_values, gender_probs = build_gender_probs(base)
    (resp_diag_terms, resp_diag_probs), (non_resp_terms, non_resp_diag_probs) = build_diagnosis_probs(base)

    resp_age_values, resp_age_probs = build_age_probs(base, 1)
    non_resp_age_values, non_resp_age_probs = build_age_probs(base, 0)

    rng = np.random.default_rng()
    sample_resp_date = build_date_sampler(base, 1, rng)
    sample_non_resp_date = build_date_sampler(base, 0, rng)

    labels_to_add = np.array([1] * add_resp + [0] * add_non_resp, dtype=int)
    rng.shuffle(labels_to_add)

    new_rows = []

    for label in labels_to_add:
        if label == 1:
            age = int(choose_weighted(rng, resp_age_values, resp_age_probs))
            diagnosis = str(choose_weighted(rng, resp_diag_terms, resp_diag_probs)).upper()
            admission_date = sample_resp_date()
        else:
            age = int(choose_weighted(rng, non_resp_age_values, non_resp_age_probs))
            diagnosis = str(choose_weighted(rng, non_resp_terms, non_resp_diag_probs)).upper()
            admission_date = sample_non_resp_date()

        gender = str(choose_weighted(rng, gender_values, gender_probs))

        locality = np.nan
        if rng.random() > locality_missing_rate:
            locality = choose_weighted(rng, locality_values, locality_probs)

        row = {
            "Patient_ID": f"{prefix}{next_id:0{id_width}d}",
            "Age_Years": float(age),
            "Gender": gender,
            "Admission_Date": pd.Timestamp(admission_date),
            "Primary_Diagnosis": diagnosis,
            "Respiratory_Label": int(label),
            "Locality": locality,
        }

        # Preserve optional columns from original schema without forcing fake data.
        for col in raw.columns:
            if col not in row:
                row[col] = np.nan

        new_rows.append(row)
        next_id += 1

    if new_rows:
        additions = pd.DataFrame(new_rows)
        additions = additions[raw.columns]
    else:
        additions = pd.DataFrame(columns=raw.columns)

    if len(additions) == 0:
        final_df = base[raw.columns].copy()
    else:
        final_df = pd.concat([base[raw.columns], additions], ignore_index=True)

    # Keep workbook order aligned with patient id progression instead of date ordering.
    final_df["_pid_num"] = pd.to_numeric(
        final_df["Patient_ID"].apply(extract_numeric_id), errors="coerce"
    )
    final_df = (
        final_df.sort_values(["_pid_num", "Patient_ID", "Admission_Date"], kind="stable")
        .drop(columns=["_pid_num"])
        .reset_index(drop=True)
    )

    if ENFORCE_CONTINUOUS_PATIENT_ID:
        output_width = max(id_width, len(str(len(final_df))))
        final_df["Patient_ID"] = [
            f"{prefix}{i:0{output_width}d}" for i in range(1, len(final_df) + 1)
        ]

    final_df["Age_Years"] = final_df["Age_Years"].astype(float)
    final_df["Respiratory_Label"] = final_df["Respiratory_Label"].astype(int)

    validation_errors = validate_final(final_df, locality_values)
    if validation_errors:
        print("\nVALIDATION FAILED:")
        for err in validation_errors:
            print(f" - {err}")
        raise ValueError("Final dataset did not pass validation. Workbook not overwritten.")

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = INPUT_FILE.with_name(f"PatientData_backup_before_expand_{timestamp}.xlsx")
    shutil.copy2(INPUT_FILE, backup_path)

    save_df = final_df.copy()
    save_df["Admission_Date"] = pd.to_datetime(
        save_df["Admission_Date"], errors="coerce"
    ).dt.strftime("%Y-%m-%d")

    with pd.ExcelWriter(
        INPUT_FILE,
        engine="openpyxl",
        date_format="YYYY-MM-DD",
        datetime_format="YYYY-MM-DD",
    ) as writer:
        save_df.to_excel(writer, index=False)

    print("\n" + "=" * 90)
    print("EXPANSION COMPLETE")
    print("=" * 90)
    print(f"Backup created: {backup_path.name}")
    print(f"Updated file: {INPUT_FILE.name}")
    print(f"Final rows: {len(final_df)}")
    print(
        f"Final respiratory/non-respiratory: "
        f"{int((final_df['Respiratory_Label'] == 1).sum())} / "
        f"{int((final_df['Respiratory_Label'] == 0).sum())}"
    )

    print("\nTop respiratory diagnoses:")
    print(
        final_df[final_df["Respiratory_Label"] == 1]["Primary_Diagnosis"]
        .value_counts()
        .head(10)
        .to_string()
    )

    print("\nTop non-respiratory diagnoses:")
    print(
        final_df[final_df["Respiratory_Label"] == 0]["Primary_Diagnosis"]
        .value_counts()
        .head(10)
        .to_string()
    )

    print("\nLocality missing rate:")
    locality_missing = final_df["Locality"].isna().mean() * 100
    print(f"{locality_missing:.1f}%")


if __name__ == "__main__":
    main()
