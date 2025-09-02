import mlflow
import pandas as pd

# Replace with your Run ID
run_id = ""
model_uri = f"runs:/{run_id}/loan_model"

# Load the model
loaded_model = mlflow.sklearn.load_model(model_uri)

# Example new loan applicant data (must match training features!)
new_data = pd.DataFrame([{
    "ApplicantIncome": 5000,
    "CoapplicantIncome": 2000,
    "LoanAmount": 150,
    "Loan_Amount_Term": 360,
    "Credit_History": 1,
    "Gender": 1,
    "Married": 1,
    "Dependents": 0,
    "Education": 1,
    "Self_Employed": 0,
    "Property_Area": 2
}])

# Predict
prediction = loaded_model.predict(new_data)
print("Prediction:", prediction)
