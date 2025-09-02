import mlflow
import mlflow.sklearn
from flask import Flask, request, jsonify
import pandas as pd

# Load the model
model = mlflow.sklearn.load_model("runs:/2a00c651e6f64e5fae58935b077046dc/model")

# Set up Flask app
app = Flask(__name__)

@app.route('/')
def index():
    return "Hello, from Flask Application"

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()  # Get input data in JSON format
    df = pd.DataFrame(data)    # Convert to pandas DataFrame
    prediction = model.predict(df)  # Make prediction
    return jsonify(prediction.tolist())  # Return prediction as JSON

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
