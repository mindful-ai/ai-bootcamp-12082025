import mlflow
import pandas as pd
import numpy as np

# -------------------------
# Load model (Registry or Run ID)
# -------------------------
# Example: load from Model Registry
# model_uri = "models:/RandomForestClassifier/Production"

# Or load directly from a run (uncomment if using run_id instead of registry)
run_id = "b24a44670d92417fb8f14274da808120"
model_uri = f"runs:/{run_id}/RandomForestClassifier"

# Load the model
loaded_model = mlflow.pyfunc.load_model(model_uri)

# Example new loan applicant data
new_data = pd.DataFrame([{
    "Gender": 1,
    "Married": 1,
    "Dependents": 0,
    "Education": 1,
    "Self_Employed": 0,
    "LoanAmount": 150,             # will be log-transformed
    "Loan_Amount_Term": 360.0,     # <-- force float
    "Credit_History": 1.0,         # <-- force float
    "Property_Area": 2,
    "TotalIncome": 7000            # will be log-transformed
}])

# Ensure numeric column types match the training schema
new_data = new_data.astype({
    "Gender": "int64",
    "Married": "int64",
    "Dependents": "int64",
    "Education": "int64",
    "Self_Employed": "int64",
    "LoanAmount": "float64",
    "Loan_Amount_Term": "float64",   # matches schema
    "Credit_History": "float64",     # matches schema
    "Property_Area": "int64",
    "TotalIncome": "float64"
})

# Apply same preprocessing as training
new_data["LoanAmount"] = np.log(new_data["LoanAmount"])
new_data["TotalIncome"] = np.log(new_data["TotalIncome"])

# Predict
prediction = loaded_model.predict(new_data)

print("Prediction:", prediction)
