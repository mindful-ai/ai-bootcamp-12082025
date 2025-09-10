# 🚀 Amazon SageMaker & SageMaker Studio Tutorial

This tutorial introduces **Amazon SageMaker**, explains **SageMaker Studio**, and walks you through a **mini project**: training and deploying a simple ML model.

---

## 🌟 1. What is Amazon SageMaker?

Amazon SageMaker is a **fully managed machine learning service** from AWS.  
It helps you **build, train, and deploy ML models** without worrying about infrastructure.  

### 🔑 Key Features
- **Data Preparation** → Clean and transform data (Data Wrangler, S3 integration).  
- **Model Building** → Use built-in algorithms or your own (PyTorch, TensorFlow, etc.).  
- **Training** → Managed compute with scaling and distributed training.  
- **Deployment** → Real-time endpoints (APIs) or batch jobs.  
- **Monitoring** → Track model performance and detect drift.  

👉 **Without SageMaker:** You must manage servers, GPUs, scaling, deployment.  
👉 **With SageMaker:** AWS does it for you with a few lines of code.  

---

## 🎨 2. What is SageMaker Studio?

**SageMaker Studio** is the **IDE (Integrated Development Environment)** for ML, running in your browser.  

### Features:
- **Jupyter Notebooks** without setup.  
- **Data Wrangler** for dataset cleaning.  
- **Training & Tuning** jobs with one click.  
- **Model Deployment** as endpoints.  
- **Experiment Tracking** to compare models.  
- **Collaboration** with Git integration.  

👉 **SageMaker = ML service**  
👉 **SageMaker Studio = Workbench (IDE) where you do ML work**  

---

## ⚙️ 3. How to Open SageMaker Studio

### Step 1: Sign in to AWS
- Go to [AWS Console](https://console.aws.amazon.com/).  

### Step 2: Open SageMaker
- Search for **SageMaker** in the AWS console.  

### Step 3: Set up SageMaker Studio
1. Click **SageMaker Studio** in the left menu.  
2. Click **Set up SageMaker Studio**.  
3. Create or choose an **IAM Role** with S3 access.  

### Step 4: Launch Studio
- Once the domain and user are created → click **Launch Studio**.  

### Step 5: Create a Notebook
- Inside Studio: **File → New → Notebook**.  
- Choose a kernel: e.g., `Python 3 (Data Science)`.  

### Step 6: Test Setup
Run this inside the notebook:

```python
import boto3
import sagemaker

# Get SageMaker session and role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

print("SageMaker is ready!")
print("Default bucket:", sagemaker_session.default_bucket())
🧪 4. Mini Project: Train & Deploy a Model
We’ll use the Iris dataset with SageMaker’s built-in XGBoost algorithm.

Step 1: Setup
python
Copy code
import sagemaker
from sagemaker import get_execution_role

sagemaker_session = sagemaker.Session()
role = get_execution_role()
bucket = sagemaker_session.default_bucket()
prefix = "iris-demo"
Step 2: Load Data & Upload to S3
python
Copy code
from sklearn.datasets import load_iris
import pandas as pd

# Load dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["label"] = iris.target

# Save CSV
df.to_csv("iris.csv", index=False, header=False)

# Upload to S3
input_data = sagemaker_session.upload_data("iris.csv", bucket=bucket, key_prefix=prefix)
print("Data uploaded to S3:", input_data)
Step 3: Train Model with XGBoost

from sagemaker.amazon.amazon_estimator import get_image_uri

# Get XGBoost container
container = get_image_uri(sagemaker_session.boto_region_name, "xgboost", "1.0-1")

# Define estimator
xgb = sagemaker.estimator.Estimator(
    container,
    role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/{prefix}/output",
    sagemaker_session=sagemaker_session,
)

# Hyperparameters
xgb.set_hyperparameters(
    objective="multi:softmax",
    num_class=3,
    num_round=50,
)

# Train
xgb.fit({"train": input_data})
Step 4: Deploy Model
python
Copy code
# Deploy the model
predictor = xgb.deploy(initial_instance_count=1, instance_type="ml.m5.large")
Step 5: Make Predictions
python
Copy code
from sagemaker.predictor import Predictor
import numpy as np

# Create predictor
predictor = Predictor(endpoint_name=predictor.endpoint_name)

# Example input (Iris flower sample)
test_sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # Iris-setosa
result = predictor.predict(test_sample)
print("Prediction:", result)
Step 6: Clean Up
python
Copy code
# Delete endpoint to avoid charges
sagemaker.Session().delete_endpoint(predictor.endpoint_name)
🎯 5. What You Learned
What SageMaker and SageMaker Studio are.

How to launch SageMaker Studio.

How to train a simple ML model using built-in XGBoost.

How to deploy the model and make predictions.

How to clean up resources.

✅ You now have a working SageMaker Studio environment and a deployed ML model!









🚀 Amazon SageMaker & SageMaker Studio Tutorial
This tutorial introduces Amazon SageMaker, explains SageMaker Studio, and walks you through a mini project: training and deploying a simple ML model.

🌟 1. What is Amazon SageMaker?
Amazon SageMaker is a fully managed machine learning (ML) service from AWS.
It helps you build, train, and deploy ML models at scale without needing to manage infrastructure.

🔑 Key Features
Data Preparation → Clean and transform data (Data Wrangler, S3 integration).

Model Building → Use built-in algorithms or your own (PyTorch, TensorFlow, etc.).

Training → Managed compute with scaling and distributed training.

Deployment → Real-time endpoints (APIs) or batch jobs.

Monitoring → Track model performance and detect drift.

📊 Why Use SageMaker?
Saves time: no server setup required.

Scales from experiments to production.

Works well with other AWS services (S3, Lambda, DynamoDB, etc.).

Supports MLOps pipelines for automation.

🎨 2. What is SageMaker Studio?
SageMaker Studio is the web-based IDE for ML.
It combines all tools needed for the ML lifecycle into one place.

Features:
Jupyter Notebooks → Run Python without setup.

Data Wrangler → Visual data prep.

Training Jobs → Managed CPU/GPU resources.

Deployment → Endpoints with scaling.

Experiment Tracking → Compare runs visually.

Collaboration → Git integration & shared workspaces.

👉 SageMaker = ML service
👉 SageMaker Studio = Workbench (IDE) where you do ML work

⚙️ 3. How to Open SageMaker Studio
Step 1: Sign in to AWS
Go to AWS Console.

Step 2: Open SageMaker
Search for SageMaker in the console.

Step 3: Set up SageMaker Studio
Click SageMaker Studio in the left menu.

Click Set up SageMaker Studio.

Choose or create an IAM Role with S3 access.

Step 4: Launch Studio
Once domain & user are created → click Launch Studio.

Step 5: Create a Notebook
Inside Studio: File → New → Notebook.

Choose a kernel: e.g., Python 3 (Data Science).

Step 6: Test Setup
python
Copy code
import boto3
import sagemaker

sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

print("SageMaker is ready!")
print("Default bucket:", sagemaker_session.default_bucket())
🧪 4. Mini Project: Train & Deploy a Model
We’ll use the Iris dataset with SageMaker’s built-in XGBoost algorithm.

Step 1: Setup
python
Copy code
import sagemaker
from sagemaker import get_execution_role

sagemaker_session = sagemaker.Session()
role = get_execution_role()
bucket = sagemaker_session.default_bucket()
prefix = "iris-demo"
Step 2: Load Data & Upload to S3
python
Copy code
from sklearn.datasets import load_iris
import pandas as pd

# Load dataset
iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df["label"] = iris.target

# Save CSV without header
df.to_csv("iris.csv", index=False, header=False)

# Upload to S3
input_data = sagemaker_session.upload_data("iris.csv", bucket=bucket, key_prefix=prefix)
print("Data uploaded to S3:", input_data)
Step 3: Train Model with XGBoost
python
Copy code
from sagemaker.amazon.amazon_estimator import get_image_uri

# Get XGBoost container
container = get_image_uri(sagemaker_session.boto_region_name, "xgboost", "1.0-1")

# Define estimator
xgb = sagemaker.estimator.Estimator(
    container,
    role,
    instance_count=1,
    instance_type="ml.m5.large",
    output_path=f"s3://{bucket}/{prefix}/output",
    sagemaker_session=sagemaker_session,
)

# Hyperparameters
xgb.set_hyperparameters(
    objective="multi:softmax",
    num_class=3,
    num_round=50,
)

# Train
xgb.fit({"train": input_data})
Step 4: Deploy Model
python
Copy code
# Deploy the model as an endpoint
predictor = xgb.deploy(initial_instance_count=1, instance_type="ml.m5.large")
Step 5: Make Predictions
python
Copy code
from sagemaker.predictor import Predictor
import numpy as np

# Create predictor
predictor = Predictor(endpoint_name=predictor.endpoint_name)

# Example input (Iris flower sample)
test_sample = np.array([[5.1, 3.5, 1.4, 0.2]])  # Iris-setosa
result = predictor.predict(test_sample)
print("Prediction:", result)
Step 6: Clean Up
python
Copy code
# Delete endpoint to avoid charges
sagemaker.Session().delete_endpoint(predictor.endpoint_name)
🎯 5. What You Learned
What SageMaker and SageMaker Studio are.

How to launch SageMaker Studio.

How to train a simple ML model using built-in XGBoost.

How to deploy the model and make predictions.

How to clean up resources.

📌 Best Practices
Always delete endpoints after use to avoid charges.

Use smaller instance types (ml.t2 or ml.m5) for testing.

Store large datasets in S3 for cost efficiency.

Track experiments with SageMaker Experiments.

For production: integrate with MLOps pipelines.

✅ You now have a working SageMaker Studio environment and a deployed ML model!

👉 To make this a downloadable file:

Open a text editor (Notepad, VS Code, etc.).

Paste the above content.

Save it as sagemaker_tutorial.md.

Would you like me to also add a section with screenshots descriptions (like "this is what the SageMaker console looks like") so it feels more like a guided workshop? 







You said:
file to download


ChatGPT said:
I can create the Markdown (.md) file content for you. Since I cannot directly give you a file download link here, I’ll provide the full .md content. You can copy it into a text editor (like Notepad or VS Code), save it with the name sagemaker_studio_tutorial.md, and it will be a proper downloadable file.

Here’s the complete file:

markdown
Copy code
# 🚀 SageMaker Studio Tutorial  
_A Beginner-Friendly Guide_

---

## 📌 Introduction  
Amazon SageMaker Studio is an **IDE (Integrated Development Environment) for Machine Learning**.  
It allows you to:  
- Build ML models  
- Train and test them  
- Deploy models as endpoints  
- Manage experiments, pipelines, and datasets  

---

## ✅ Prerequisites  
Before starting, make sure you have:  
1. An **AWS account** (with billing enabled).  
2. Basic knowledge of Python.  
3. IAM permissions for SageMaker and S3.  

---

## 📝 Steps to Set Up SageMaker Studio  

### Step 1: Sign in to AWS
- Go to [AWS Console](https://console.aws.amazon.com/).  
- Log in with your AWS account (Root user or IAM user).  

---

### Step 2: Open SageMaker
- In the **search bar**, type `SageMaker`.  
- Click **Amazon SageMaker**.  
- You’ll see the **SageMaker Dashboard**.  

---

### Step 3: Set up SageMaker Studio
1. In the left menu, select **SageMaker Studio**.  
2. Click **Set up SageMaker Studio**.  
3. Choose an **execution role**:  
   - If you’re new, select **Create a new role** → choose default permissions.  
   - SageMaker needs access to **S3** (to store data).  

---

### Step 4: Launch SageMaker Studio
- Once the domain and user are created, click **Launch Studio**.  
- A new tab will open with **SageMaker Studio interface** (similar to JupyterLab).  

---

### Step 5: Create a Notebook
1. Inside SageMaker Studio, click:  
   - **File → New → Notebook**  
2. Select a **kernel**, for example:  
   - `Python 3 (Data Science)`  
   - `Python 3 (PyTorch CPU)`  

A new Jupyter notebook will open.  

---

### Step 6: Verify Setup with Python Code
Run this inside the notebook:  

```python
import boto3
import sagemaker

# Get SageMaker session and role
sagemaker_session = sagemaker.Session()
role = sagemaker.get_execution_role()

print("✅ SageMaker is ready!")
print("📦 Default bucket:", sagemaker_session.default_bucket())
If this prints the default S3 bucket, SageMaker is correctly set up 🎉.

📊 Mini Project: Train a Simple Model
We’ll use the Iris dataset to train a simple model inside SageMaker.

Step 1: Import Libraries
python
Copy code
from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import joblib
import boto3
import sagemaker
import os
Step 2: Load and Split Data
python
Copy code
iris = load_iris()
X_train, X_test, y_train, y_test = train_test_split(
    iris.data, iris.target, test_size=0.2, random_state=42
)
Step 3: Train Model
python
Copy code
model = RandomForestClassifier(n_estimators=100)
model.fit(X_train, y_train)

print("✅ Training complete. Accuracy:", model.score(X_test, y_test))
Step 4: Save Model
python
Copy code
# Save model locally
joblib.dump(model, "iris_model.pkl")

# Upload model to S3
sagemaker_session = sagemaker.Session()
bucket = sagemaker_session.default_bucket()
prefix = "iris-model"

s3_path = sagemaker_session.upload_data("iris_model.pkl", bucket=bucket, key_prefix=prefix)
print("📦 Model uploaded to S3:", s3_path)
🚀 Deploy the Model in SageMaker
You can deploy the trained model as an endpoint.

Step 1: Define Model
python
Copy code
from sagemaker.sklearn.model import SKLearnModel

role = sagemaker.get_execution_role()

sklearn_model = SKLearnModel(
    model_data=s3_path,
    role=role,
    entry_point="inference.py",  # custom script for inference
    framework_version="0.23-1"
)
Step 2: Deploy Endpoint
python
Copy code
predictor = sklearn_model.deploy(
    initial_instance_count=1,
    instance_type="ml.m5.large"
)
Step 3: Test Prediction
python
Copy code
result = predictor.predict(X_test[:5])
print("🔮 Predictions:", result)
⚠️ Shutdown to Save Costs
When finished:

Go to SageMaker → Studio → Domains

Shut down Studio

Delete unused endpoints and instances

🎯 Summary
In this tutorial, you:

Set up SageMaker Studio

Created a Jupyter notebook

Trained and saved a model

Uploaded it to S3

Deployed it as a real-time endpoint

Amazon SageMaker Studio makes it much easier to build, train, and deploy ML models end-to-end in the cloud.


