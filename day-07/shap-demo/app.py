
import os
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, roc_auc_score, confusion_matrix
import shap
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Approval SHAP Demo", layout="wide")
st.title("🏦 Loan Approval Prediction + SHAP Explainability")

st.markdown("""
This demo trains a **Random Forest** to predict **loan default risk** on the **German Credit** dataset and uses **SHAP** to explain:
- **Global** feature importance (across the dataset).
- **Local** explanations (for a single applicant).

**Tip for speed:** We compute SHAP on a small sample (default 400 rows).
""")

@st.cache_data(show_spinner=True)
def load_data():
    # Try OpenML German Credit (credit-g). Fallback to a tiny synthetic dataset.
    try:
        from sklearn.datasets import fetch_openml
        df = fetch_openml("credit-g", version=1, as_frame=True).frame
        # Target is 'class': 'good'/'bad'. We'll convert to 1=good, 0=bad
        df["target"] = (df["class"] == "good").astype(int)
        df = df.drop(columns=["class"])
        return df, "openml"
    except Exception as e:
        # Synthetic fallback (small)
        rng = np.random.RandomState(42)
        n = 400
        df = pd.DataFrame({
            "duration": rng.randint(4, 60, size=n),
            "amount": rng.randint(500, 20000, size=n),
            "age": rng.randint(18, 75, size=n),
            "employment": rng.choice(["unemployed","<1yr","1-4yrs","4-7yrs",">=7yrs"], size=n, p=[0.1,0.2,0.35,0.2,0.15]),
            "housing": rng.choice(["own","rent","free"], size=n, p=[0.6,0.35,0.05]),
            "savings": rng.choice(["little","moderate","rich"], size=n, p=[0.6,0.3,0.1]),
            "purpose": rng.choice(["car","furniture/equipment","radio/tv","education","business","domestic appliances"], size=n),
        })
        # Rule-of-thumb synthetic label: higher amount & duration, lower savings => higher default risk
        score = (df["amount"]/20000) + (df["duration"]/60) - (df["savings"].map({"little":0.2,"moderate":0.0,"rich":-0.2}))
        y = (score < 0.8).astype(int)  # 1 = approve/good, 0 = bad
        df["target"] = y
        return df, "synthetic"

df, source = load_data()
st.info(f"Data source: **{source}** | Shape: {df.shape}")

# Identify feature columns
target_col = "target"
feature_cols = [c for c in df.columns if c != target_col]

# Split train/test
test_size = st.sidebar.slider("Test size", 0.1, 0.4, 0.2, 0.05)
random_state = st.sidebar.number_input("Random state", value=42, step=1)

X_train, X_test, y_train, y_test = train_test_split(
    df[feature_cols], df[target_col], test_size=test_size, random_state=random_state, stratify=df[target_col]
)

# Separate dtypes
cat_cols = [c for c in X_train.columns if X_train[c].dtype == "object"]
num_cols = [c for c in X_train.columns if c not in cat_cols]

# Preprocessor
preprocess = ColumnTransformer(transformers=[
    ("num", Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]), num_cols),
    ("cat", Pipeline([("impute", SimpleImputer(strategy="most_frequent")), ("oh", OneHotEncoder(handle_unknown="ignore"))]), cat_cols),
])

# Model hyperparams
n_estimators = st.sidebar.slider("RandomForest n_estimators", 100, 800, 300, 50)
max_depth = st.sidebar.slider("RandomForest max_depth (None=0)", 0, 30, 0, 1)
rf_kwargs = {"n_estimators": n_estimators, "random_state": random_state, "n_jobs": -1}
if max_depth > 0:
    rf_kwargs["max_depth"] = max_depth

pipe = Pipeline([
    ("pre", preprocess),
    ("clf", RandomForestClassifier(**rf_kwargs))
])

# Train
with st.spinner("Training model..."):
    pipe.fit(X_train, y_train)

# Evaluate
y_pred = pipe.predict(X_test)
y_prob = pipe.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_prob)
st.subheader("📈 Performance")
st.write(f"ROC-AUC: **{auc:.3f}**")
st.text("Classification report:")
st.text(classification_report(y_test, y_pred, digits=3))

st.write("Confusion matrix:")
cm = confusion_matrix(y_test, y_pred)
st.write(pd.DataFrame(cm, index=["Actual 0","Actual 1"], columns=["Pred 0","Pred 1"]))

# SHAP explanations
st.subheader("🧠 SHAP Explainability")

# Sample for speed
sample_size = st.slider("SHAP sample size", 100, min(1000, len(X_test)), min(400, len(X_test)), 50)
sample_idx = np.random.RandomState(random_state).choice(len(X_test), size=sample_size, replace=False)
X_sample = X_test.iloc[sample_idx]

# Transform once for efficiency
X_train_trans = pipe.named_steps["pre"].fit_transform(X_train)  # already fit, but ensure transform matrix
X_sample_trans = pipe.named_steps["pre"].transform(X_sample)

# Feature names after preprocessing
def get_feature_names(preprocess, numeric, categoricals):
    num_feats = numeric
    cat_transformer = preprocess.named_transformers_["cat"]
    oh = cat_transformer.named_steps["oh"]
    cat_feats = list(oh.get_feature_names_out(categoricals))
    return num_feats + cat_feats

feature_names = get_feature_names(preprocess, num_cols, cat_cols)

# Use fast SHAP
with st.spinner("Computing SHAP values (fast mode)..."):
    explainer = shap.Explainer(pipe.named_steps["clf"], X_train_trans, algorithm="tree")
    shap_values = explainer(X_sample_trans, check_additivity=False)

col1, col2 = st.columns(2)
with col1:
    st.write("Global Importance (SHAP Beeswarm):")
    fig1 = plt.figure(figsize=(6,4))
    shap.summary_plot(shap_values, X_sample_trans, feature_names=feature_names, show=False)
    st.pyplot(fig1, clear_figure=True)

with col2:
    st.write("Mean |SHAP| (Bar Plot):")
    fig2 = plt.figure(figsize=(6,4))
    shap.summary_plot(shap_values, X_sample_trans, feature_names=feature_names, plot_type="bar", show=False)
    st.pyplot(fig2, clear_figure=True)

st.markdown("---")
st.subheader("🔍 Explain a Single Applicant")

# Build a UI to pick a single row or enter custom values
mode = st.radio("Choose one:", ["Pick from test set", "Enter custom applicant"])

def build_input_from_row(row: pd.Series) -> pd.DataFrame:
    return pd.DataFrame([row.to_dict()])[feature_cols]

if mode == "Pick from test set":
    idx = st.number_input("Row index in test set", min_value=0, max_value=len(X_test)-1, value=0, step=1)
    x_row = X_test.iloc[int(idx)]
    st.write("Selected applicant features:")
    st.write(pd.DataFrame([x_row]))
else:
    # Simple UI for a subset of features (fallback to defaults)
    inputs = {}
    for c in num_cols[:6]:  # limit UI to first 6 numeric for brevity
        default_val = float(X_train[c].median()) if np.issubdtype(X_train[c].dtype, np.number) else 0.0
        inputs[c] = st.number_input(f"{c}", value=default_val)
    for c in cat_cols[:6]:  # limit UI to first 6 categorical for brevity
        options = ["<missing>"] + sorted([str(v) for v in pd.Series(X_train[c].unique()).dropna().unique().tolist()])
        val = st.selectbox(f"{c}", options, index=0)
        inputs[c] = (None if val == "<missing>" else val)
    x_row = pd.Series(inputs)

# Prepare single row for prediction
x_df = build_input_from_row(x_row)
proba = pipe.predict_proba(x_df)[0,1]
pred  = pipe.predict(x_df)[0]

st.write(f"**Predicted approval probability (class=1 good): {proba:.3f}** | Predicted class: **{pred}**")

# SHAP for single row
x_row_trans = pipe.named_steps["pre"].transform(x_df)
with st.spinner("Computing SHAP for this applicant..."):
    sv_row = explainer(x_row_trans, check_additivity=False)

# Show top positive/negative contributors
vals = sv_row.values[0] if hasattr(sv_row, "values") else sv_row[0].values
abs_idx = np.argsort(np.abs(vals))[::-1][:10]
top_df = pd.DataFrame({
    "feature": np.array(feature_names)[abs_idx],
    "shap_value": vals[abs_idx]
})
st.write("Top contributing features for this prediction:")
st.dataframe(top_df)

st.caption("Note: For categorical variables, features are one-hot encoded (feature=value). Positive SHAP values push towards class 1 (good), negative towards class 0 (bad).")
