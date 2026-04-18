import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.metrics import roc_auc_score, f1_score, recall_score, precision_score
import xgboost as xgb
import shap
import warnings
warnings.filterwarnings('ignore')

def main():
    print("🚀 STARTING MANUSCRIPT EXPANSION DATA GENERATOR")
    print("="*80)
    
    # Load Data
    df = pd.read_csv("Analysis_Ready_Dataset.csv")
    df['Admission_Date'] = pd.to_datetime(df['Admission_Date'])
    
    print("\n📊 PART 1: EXPLORATORY DATA ANALYSIS (TABLE 1)")
    
    # Table 1 stats
    resp = df[df['Respiratory_Label'] == 1]
    non_resp = df[df['Respiratory_Label'] == 0]
    
    print("--------------------------------------------------")
    print("TABLE 1: Baseline Characteristics")
    print("--------------------------------------------------")
    print(f"Total N = {len(df)}")
    print(f"Respiratory N = {len(resp)} ({len(resp)/len(df)*100:.1f}%)")
    print(f"Non-Respiratory N = {len(non_resp)} ({len(non_resp)/len(df)*100:.1f}%)")
    print(f"\nAge (years):")
    print(f"  Overall: {df['Age_Years'].mean():.1f} ± {df['Age_Years'].std():.1f}")
    print(f"  Respiratory: {resp['Age_Years'].mean():.1f} ± {resp['Age_Years'].std():.1f}")
    print(f"  Non-Respiratory: {non_resp['Age_Years'].mean():.1f} ± {non_resp['Age_Years'].std():.1f}")
    
    if 'Gender' in df.columns:
        print("\nGender (Male/Female %):")
        m_r = (resp['Gender'] == 'M').sum() / len(resp)
        m_nr = (non_resp['Gender'] == 'M').sum() / len(non_resp)
        print(f"  Respiratory: {m_r*100:.1f}% Male")
        print(f"  Non-Respiratory: {m_nr*100:.1f}% Male")
        
    print("\nMean Pollution Exposures:")
    for pol in ['PM2_5', 'PM10', 'NO2']:
        print(f"  {pol} -> Overall: {df[pol].mean():.1f}, Resp: {resp[pol].mean():.1f}, Non-Resp: {non_resp[pol].mean():.1f}")
        
    print("\nGenerating Figure: Time-series of PM2.5 vs Respiratory Admissions...")
    # Group timeline
    daily_pm = df.groupby('Admission_Date')['PM2_5'].mean()
    daily_adm = df[df['Respiratory_Label'] == 1].groupby('Admission_Date').size()
    
    fig, ax1 = plt.subplots(figsize=(12, 5))
    ax1.plot(daily_pm.index, daily_pm.values, color='firebrick', alpha=0.7, label='Mean PM2.5 (µg/m³)')
    ax1.set_ylabel('PM2.5 Concentration', color='firebrick')
    ax1.tick_params(axis='y', labelcolor='firebrick')
    
    ax2 = ax1.twinx()
    ax2.bar(daily_adm.index, daily_adm.values, color='steelblue', alpha=0.5, label='Respiratory Admissions', width=1)
    ax2.set_ylabel('Daily Respiratory Admission Count', color='steelblue')
    ax2.tick_params(axis='y', labelcolor='steelblue')
    
    plt.title("Daily PM2.5 Concentration and Pediatric Respiratory Admissions (Feb 2025 - Jan 2026)")
    fig.tight_layout()
    plt.savefig("Research/DONE/figures/eda_timeseries.png", dpi=300)
    plt.close()
    print("✅ EDA Time-series saved to Research/DONE/figures/eda_timeseries.png")
    
    print("\n💥 PART 2: ABLATION STUDY (Removing Age and Day_of_Week)")
    print("="*80)
    
    # Prepare data for Ablation
    # Drop standard exclusions
    base_drop = ['Patient_ID', 'Admission_Date', 'Primary_Diagnosis', 'Locality']
    X_full = df.drop(columns=[c for c in base_drop if c in df.columns] + ['Respiratory_Label'])
    y = df['Respiratory_Label']
    
    # ABLATION DROP: Behavioral and Demographic core drivers
    ablation_drop = ['Age_Years', 'Age_Group', 'Day_of_Week', 'Month']
    X_ablated = X_full.drop(columns=[c for c in ablation_drop if c in X_full.columns])
    
    print(f"Original features count: {len(X_full.columns)}")
    print(f"Ablated features count: {len(X_ablated.columns)}")
    print(f"Dropped: {ablation_drop}")
    
    # Setup transformer for ablated data
    num_ab = ['PM2_5', 'PM10', 'NO2', 'PM2_5_Lag1', 'PM2_5_Lag7', 'PM10_Lag1', 'PM10_Lag7', 'NO2_Lag1', 'NO2_Lag7', 'Week_of_Year', 'Day_of_Year']
    cat_ab = ['Gender', 'Season', 'Quarter']
    
    num_ab = [f for f in num_ab if f in X_ablated.columns]
    cat_ab = [f for f in cat_ab if f in X_ablated.columns]
    
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), num_ab),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), cat_ab)
        ], remainder='passthrough'
    )
    
    # Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(X_ablated, y, test_size=0.20, stratify=y, random_state=42)
    
    X_tr_proc = preprocessor.fit_transform(X_train)
    X_ts_proc = preprocessor.transform(X_test)
    
    feat_names = num_ab + list(preprocessor.named_transformers_['cat'].get_feature_names_out(cat_ab))
    X_tr_df = pd.DataFrame(X_tr_proc, columns=feat_names)
    X_ts_df = pd.DataFrame(X_ts_proc, columns=feat_names)
    
    pos_w = (y_train == 0).sum() / (y_train == 1).sum()
    ablated_model = xgb.XGBClassifier(scale_pos_weight=pos_w, random_state=42, eval_metric="logloss")
    ablated_model.fit(X_tr_df, y_train)
    
    y_prob = ablated_model.predict_proba(X_ts_df)[:, 1]
    y_pred = ablated_model.predict(X_ts_df)
    
    auc = roc_auc_score(y_test, y_prob)
    print(f"\nAblated Model ROC-AUC: {auc:.3f} (Baseline was ~0.775)")
    print(f"Ablated Model Recall: {recall_score(y_test, y_pred):.3f}")
    
    # SHAP for Ablated Model
    explainer = shap.TreeExplainer(ablated_model)
    shap_values = explainer.shap_values(X_ts_df)
    
    if isinstance(shap_values, list) and len(shap_values) == 2: 
        shap_values = shap_values[1]
        
    fig, ax = plt.subplots(figsize=(10, 6))
    shap.summary_plot(shap_values, X_ts_df, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig("Research/DONE/figures/shap_ablation_summary.png", dpi=300)
    plt.close()
    
    print("✅ Ablated SHAP figure saved to Research/DONE/figures/shap_ablation_summary.png")
    print("="*80)
    print("🎉 GENERATOR COMPLETE")

if __name__ == "__main__":
    main()
