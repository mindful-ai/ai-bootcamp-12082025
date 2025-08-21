
# Loan Approval + SHAP Explainability (Streamlit App)

This is a complete, classroom-ready app that:
- Loads the **German Credit** dataset from OpenML (loan good/bad).  
- Trains a **RandomForestClassifier** in a scikit-learn **Pipeline** with preprocessing.  
- Computes **fast SHAP** explanations:
  - Global importance (beeswarm + bar).
  - Local explanation for a single applicant.

## Quickstart

```bash
pip install -r requirements.txt
streamlit run app.py
```

> If OpenML is unavailable, the app falls back to a small **synthetic** dataset so you can still demo the flow.

## Files
- `app.py` — Streamlit app
- `requirements.txt`
- `loan_shap_demo.ipynb` — Jupyter notebook version of the same workflow

## What you'll teach
- Train/test split, preprocessing (numeric + categorical) with `ColumnTransformer`
- Model training & metrics (ROC-AUC, confusion matrix, classification report)
- **SHAP**: global + local explanations, fast settings for workshops

## Notes
- SHAP can be slow. This app computes SHAP on a **sample** of the test set and uses `shap.Explainer(..., algorithm="tree")` with `check_additivity=False` for speed.
