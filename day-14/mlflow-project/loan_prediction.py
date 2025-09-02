import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from matplotlib import pyplot as plt
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn import metrics
import mlflow
import mlflow.sklearn
import os
from mlflow.models.signature import infer_signature

# Load the dataset
dataset = pd.read_csv("train.csv")

numerical_cols = dataset.select_dtypes(include=['int64','float64']).columns.tolist()
categorical_cols = dataset.select_dtypes(include=['object']).columns.tolist()
categorical_cols.remove('Loan_Status')
categorical_cols.remove('Loan_ID')

# Fill missing values
for col in categorical_cols:
    dataset[col] = dataset[col].fillna(dataset[col].mode()[0])

for col in numerical_cols:
    dataset[col] = dataset[col].fillna(dataset[col].median())

# Handle outliers
dataset[numerical_cols] = dataset[numerical_cols].apply(lambda x: x.clip(*x.quantile([0.05, 0.95])))

# Log Transformation & Feature Engineering
dataset['LoanAmount'] = np.log(dataset['LoanAmount'])
dataset['TotalIncome'] = dataset['ApplicantIncome'] + dataset['CoapplicantIncome']
dataset['TotalIncome'] = np.log(dataset['TotalIncome'])

# Drop redundant cols
dataset = dataset.drop(columns=['ApplicantIncome','CoapplicantIncome'])

# Encode categoricals
for col in categorical_cols:
    le = LabelEncoder()
    dataset[col] = le.fit_transform(dataset[col])

# Encode target
le = LabelEncoder()
dataset['Loan_Status'] = le.fit_transform(dataset['Loan_Status'])

# Train/test split
X = dataset.drop(columns=['Loan_Status', 'Loan_ID'])
y = dataset.Loan_Status
RANDOM_SEED = 6

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=RANDOM_SEED)

# Define models + params
rf = RandomForestClassifier(random_state=RANDOM_SEED)
param_grid_forest = {
    'n_estimators': [200, 400, 700],
    'max_depth': [10, 20, 30],
    'criterion': ["gini", "entropy"],
    'max_leaf_nodes': [50, 100]
}
grid_forest = GridSearchCV(rf, param_grid_forest, cv=5, n_jobs=-1, scoring='accuracy')

lr = LogisticRegression(random_state=RANDOM_SEED)
param_grid_log = {
    'C': [100, 10, 1.0, 0.1, 0.01],
    'penalty': ['l1', 'l2'],
    'solver': ['liblinear']
}
grid_log = GridSearchCV(lr, param_grid_log, cv=5, n_jobs=-1, scoring='accuracy')

dt = DecisionTreeClassifier(random_state=RANDOM_SEED)
param_grid_tree = {
    "max_depth": [3, 5, 7, 9, 11, 13],
    'criterion': ["gini", "entropy"],
}
grid_tree = GridSearchCV(dt, param_grid_tree, cv=5, n_jobs=-1, scoring='accuracy')

# Fit models
model_forest = grid_forest.fit(X_train, y_train)
model_log = grid_log.fit(X_train, y_train)
model_tree = grid_tree.fit(X_train, y_train)

mlflow.set_experiment("Loan_prediction")

# Evaluation function
def eval_metrics(actual, pred):
    accuracy = metrics.accuracy_score(actual, pred)
    f1 = metrics.f1_score(actual, pred, pos_label=1)
    fpr, tpr, _ = metrics.roc_curve(actual, pred)
    auc = metrics.auc(fpr, tpr)

    plt.figure(figsize=(8,8))
    plt.plot(fpr, tpr, color='blue', label=f'ROC curve area = {auc:.2f}')
    plt.plot([0,1],[0,1], 'r--')
    plt.xlabel('False Positive Rate', size=14)
    plt.ylabel('True Positive Rate', size=14)
    plt.legend(loc='lower right')
    os.makedirs("plots", exist_ok=True)
    plt.savefig("plots/ROC_curve.png")
    plt.close()

    return accuracy, f1, auc

# MLflow logging function
def mlflow_logging(model, X, y, name):
    best_model = model.best_estimator_
    pred = best_model.predict(X)
    (accuracy, f1, auc) = eval_metrics(y, pred)
    signature = infer_signature(X, pred)

    with mlflow.start_run():
        mlflow.set_tag("model_name", name)
        mlflow.log_params(model.best_params_)
        mlflow.log_metric("Mean CV score", model.best_score_)
        mlflow.log_metric("Accuracy", accuracy)
        mlflow.log_metric("f1-score", f1)
        mlflow.log_metric("AUC", auc)
        mlflow.log_artifact("plots/ROC_curve.png")
        mlflow.sklearn.log_model(
            best_model,
            artifact_path=name,
            input_example=X[:5],
            signature=signature
        )

# Log all models
mlflow_logging(model_tree, X_test, y_test, "DecisionTreeClassifier")
mlflow_logging(model_log, X_test, y_test, "LogisticRegression")
mlflow_logging(model_forest, X_test, y_test, "RandomForestClassifier")
