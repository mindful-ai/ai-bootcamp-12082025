import mlflow
from sklearn.datasets import load_diabetes
logged_model = 'runs:/2a00c651e6f64e5fae58935b077046dc/model'

# Load model as a PyFuncModel.
loaded_model = mlflow.pyfunc.load_model(logged_model)
data = load_diabetes()
print(data.data[0])

# Predict on a Pandas DataFrame.
import pandas as pd
print(loaded_model.predict([data.data[0]]))