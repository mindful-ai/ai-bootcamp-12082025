mlflow models serve -m runs:/<your_run_id>/loan_model -p 1234

curl -X POST http://127.0.0.1:1234/invocations \
    -H 'Content-Type: application/json' \
    -d '{
        "data": [{
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
        }]
    }'
