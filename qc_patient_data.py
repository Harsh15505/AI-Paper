import pandas as pd


def normalize_locality(series):
    return (
        series.astype(str)
        .str.strip()
        .replace(
            {
                "": pd.NA,
                "nan": pd.NA,
                "NAN": pd.NA,
                "None": pd.NA,
                "NONE": pd.NA,
                "NULL": pd.NA,
                "null": pd.NA,
            }
        )
    )


def main():
    df = pd.read_excel("PatientData.xlsx")
    orig = pd.read_excel("PatientData_backup_before_expand_20260418_001357.xlsx")

    crit = ["Admission_Date", "Age_Years", "Respiratory_Label"]

    date_series = pd.to_datetime(df["Admission_Date"], errors="coerce")

    print("rows", len(df))
    print("resp_counts", df["Respiratory_Label"].value_counts().to_dict())
    print("date_min", date_series.min(), "date_max", date_series.max())
    print("age_min", df["Age_Years"].min(), "age_max", df["Age_Years"].max())
    print("missing_critical", df[crit].isna().sum().to_dict())

    locality_clean = normalize_locality(df["Locality"])
    print("locality_missing", int(locality_clean.isna().sum()))

    orig_scope = orig.dropna(subset=crit).copy()
    orig_scope["Admission_Date"] = pd.to_datetime(orig_scope["Admission_Date"], errors="coerce")
    orig_scope = orig_scope[
        (orig_scope["Age_Years"] >= 2)
        & (orig_scope["Age_Years"] <= 12)
        & (orig_scope["Admission_Date"] >= pd.Timestamp("2025-02-01"))
        & (orig_scope["Admission_Date"] <= pd.Timestamp("2026-01-31"))
    ]

    whitelist = normalize_locality(orig_scope["Locality"]).dropna()
    extra_localities = sorted(set(locality_clean.dropna()) - set(whitelist))
    print("extra_localities", extra_localities)

    month_counts = date_series.dt.to_period("M").astype(str).value_counts().sort_index().to_dict()
    print("month_counts", month_counts)
    print("gender_counts", df["Gender"].value_counts(dropna=False).to_dict())
    print("age_counts", df["Age_Years"].value_counts().sort_index().to_dict())


if __name__ == "__main__":
    main()
