import os
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, f1_score, confusion_matrix, precision_score, recall_score
import xgboost as xgb
import shap

def main():
    print("🚀 STARTING MODELING PIPELINE")
    print("="*80)
    
    # 1. Setup paths
    os.makedirs("Research/DONE/figures", exist_ok=True)
    
    # 2. Load Data
    try:
        df = pd.read_csv("Analysis_Ready_Dataset.csv")
        print(f"✅ Loaded dataset: {len(df)} records")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return

    # 3. Preprocess Features
    # Drop irrelevant/identifier columns and those with high missingness 
    cols_to_drop = ['Patient_ID', 'Admission_Date', 'Primary_Diagnosis', 'Locality']
    df = df.drop(columns=[c for c in cols_to_drop if c in df.columns])
    
    # Target
    y = df['Respiratory_Label']
    X = df.drop(columns=['Respiratory_Label'])
    
    # Identify Categorical and Numerical features
    numeric_features = [
        'Age_Years', 'PM2_5', 'PM10', 'NO2', 
        'PM2_5_Lag1', 'PM2_5_Lag7', 'PM10_Lag1', 'PM10_Lag7', 'NO2_Lag1', 'NO2_Lag7',
        'Month', 'Week_of_Year', 'Day_of_Week', 'Day_of_Year'
    ]
    numeric_features = [f for f in numeric_features if f in X.columns]
    
    categorical_features = ['Gender', 'Season', 'Age_Group', 'Quarter']
    categorical_features = [f for f in categorical_features if f in X.columns]
    
    print("\n🧹 Feature Setup")
    print(f"   Numeric Features: {len(numeric_features)}")
    print(f"   Categorical Features: {len(categorical_features)}")
    
    # Build Preprocessor
    preprocessor = ColumnTransformer(
        transformers=[
            ('num', StandardScaler(), numeric_features),
            ('cat', OneHotEncoder(drop='first', sparse_output=False), categorical_features)
        ],
        remainder='passthrough'
    )
    
    # 4. Train/Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.20, stratify=y, random_state=42
    )
    print(f"\n✂️ Train/Test Split (80/20)")
    print(f"   Train size: {len(X_train)} | Test size: {len(X_test)}")
    
    # Fit and transform features
    X_train_processed = preprocessor.fit_transform(X_train)
    X_test_processed = preprocessor.transform(X_test)
    
    # Get feature names after OHE
    ohe_feature_names = preprocessor.named_transformers_['cat'].get_feature_names_out(categorical_features)
    feature_names = numeric_features + list(ohe_feature_names)
    
    # Remap DataFrames safely for SHAP later
    X_train_processed = pd.DataFrame(X_train_processed, columns=feature_names)
    X_test_processed = pd.DataFrame(X_test_processed, columns=feature_names)

    # 5. Define Models
    pos_weight = (y_train == 0).sum() / (y_train == 1).sum()
    
    models = {
        "Logistic Regression": LogisticRegression(class_weight='balanced', random_state=42, max_iter=1000),
        "Random Forest": RandomForestClassifier(class_weight='balanced', random_state=42, n_estimators=200),
        "XGBoost": xgb.XGBClassifier(scale_pos_weight=pos_weight, random_state=42, eval_metric="logloss")
    }
    
    # 6. Train and Evaluate
    print("\n🤖 Training and Evaluating Models")
    print("="*80)
    
    best_model_name = None
    best_auc = 0
    best_model = None
    
    for name, model in models.items():
        model.fit(X_train_processed, y_train)
        y_pred = model.predict(X_test_processed)
        y_prob = model.predict_proba(X_test_processed)[:, 1] if hasattr(model, "predict_proba") else y_pred
        
        auc = roc_auc_score(y_test, y_prob)
        f1 = f1_score(y_test, y_pred)
        rec = recall_score(y_test, y_pred)
        prec = precision_score(y_test, y_pred)
        
        print(f"➡️ {name}:")
        print(f"   ROC-AUC : {auc:.3f}")
        print(f"   F1-Score: {f1:.3f}")
        print(f"   Recall  : {rec:.3f}")
        print(f"   Precis. : {prec:.3f}")
        
        # Save best model based on ROC-AUC
        if auc > best_auc:
            best_auc = auc
            best_model = model
            best_model_name = name

    print(f"\n🏆 Best Model Selected: {best_model_name} (ROC-AUC: {best_auc:.3f})")
    
    # 7. Model Interpretation using SHAP
    print("\n🔍 Generating SHAP Values and Visualizations...")
    
    if best_model_name in ["Random Forest", "XGBoost"]:
        explainer = shap.TreeExplainer(best_model)
        shap_values = explainer.shap_values(X_test_processed)
        
        # XGBoost output might be 2D or 1D depending on objective, adjust for shap
        if isinstance(shap_values, list) and len(shap_values) == 2: 
            shap_values = shap_values[1] # Keep only positive class shap values
            
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.summary_plot(shap_values, X_test_processed, plot_type="bar", show=False)
        plt.tight_layout()
        plt.savefig("Research/DONE/figures/shap_summary_bar.png", dpi=300)
        plt.close()
        
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.summary_plot(shap_values, X_test_processed, show=False)
        plt.tight_layout()
        plt.savefig("Research/DONE/figures/shap_summary_dot.png", dpi=300)
        plt.close()
        
        # Select single instance (e.g. index 0)
        # We need shap.Explanation object for waterfall
        expected_value = explainer.expected_value
        if isinstance(expected_value, list) or isinstance(expected_value, np.ndarray):
            expected_value = expected_value[-1] # take positive class
            
        # Try to generate waterfall plot safely
        try:
            explanation = shap.Explanation(values=shap_values[0], base_values=expected_value, data=X_test_processed.iloc[0], feature_names=feature_names)
            shap.waterfall_plot(explanation, show=False)
            plt.tight_layout()
            plt.savefig("Research/DONE/figures/shap_waterfall_local.png", dpi=300)
            plt.close()
        except Exception as e:
            print(f"⚠️ Could not generate waterfall plot: {e}")
            
    elif best_model_name == "Logistic Regression":
        explainer = shap.LinearExplainer(best_model, X_train_processed)
        shap_values = explainer.shap_values(X_test_processed)
        fig, ax = plt.subplots(figsize=(10, 6))
        shap.summary_plot(shap_values, X_test_processed, show=False)
        plt.tight_layout()
        plt.savefig("Research/DONE/figures/shap_summary_lr.png", dpi=300)
        plt.close()

    print("✅ SHAP Visualizations saved to Research/DONE/figures/")
    print("\n" + "="*80)
    print("🎉 MODELING PIPELINE COMPLETE!")

if __name__ == "__main__":
    main()
