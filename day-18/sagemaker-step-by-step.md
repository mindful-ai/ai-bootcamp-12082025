# SageMaker Beginner Example --- Step-by-Step Guide

This guide walks you through setting up and running a beginner SageMaker
example, starting from initial configuration to cleanup.

------------------------------------------------------------------------

## Prerequisites

1.  An AWS account with permissions for IAM, S3, and SageMaker.
2.  AWS CLI installed and configured (`aws configure`).
3.  (Optional) Python 3.8+ with pip if running locally.

------------------------------------------------------------------------

## Step 0 --- Choose a Region

Pick a region, e.g., `ap-south-1` or `us-east-1`. Use this consistently
for S3, SageMaker, and IAM.

------------------------------------------------------------------------

## Step 1 --- Create IAM Role for SageMaker

Create a trust policy file `trust.json`:

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": { "Service": "sagemaker.amazonaws.com" },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

Create role and attach policies:

``` bash
aws iam create-role --role-name MySageMakerRole --assume-role-policy-document file://trust.json
aws iam attach-role-policy --role-name MySageMakerRole --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
aws iam attach-role-policy --role-name MySageMakerRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

------------------------------------------------------------------------

## Step 2 --- Create an S3 Bucket

``` bash
aws s3 mb s3://my-sagemaker-bucket-<unique> --region ap-south-1
```

------------------------------------------------------------------------

## Step 3 --- Training Script `train.py`

``` python
import argparse, os, pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import joblib

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--train', type=str, default='/opt/ml/input/data/train')
    args = parser.parse_args()

    df = pd.read_csv(os.path.join(args.train, 'iris.csv'))
    X = df.drop('target', axis=1)
    y = df['target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100)
    clf.fit(X_train, y_train)
    preds = clf.predict(X_test)
    print("Test accuracy:", accuracy_score(y_test, preds))

    os.makedirs('/opt/ml/model', exist_ok=True)
    joblib.dump(clf, '/opt/ml/model/model.joblib')
```

------------------------------------------------------------------------

## Step 4 --- Install Dependencies

``` bash
pip install sagemaker boto3 scikit-learn pandas joblib
```

------------------------------------------------------------------------

## Step 5 --- Prepare Dataset

``` python
from sklearn.datasets import load_iris
import pandas as pd

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df.to_csv('iris.csv', index=False)
```

Upload to S3:

``` bash
aws s3 cp iris.csv s3://my-sagemaker-bucket-<unique>/sagemaker/iris-example/train/iris.csv
```

------------------------------------------------------------------------

## Step 6A --- Run in SageMaker Studio

``` python
import sagemaker
from sagemaker.sklearn.estimator import SKLearn
from sagemaker import get_execution_role
from sklearn.datasets import load_iris
import pandas as pd

sess = sagemaker.Session()
role = get_execution_role()
bucket = sess.default_bucket()
prefix = 'sagemaker/iris-example'

iris = load_iris()
df = pd.DataFrame(iris.data, columns=iris.feature_names)
df['target'] = iris.target
df.to_csv('iris.csv', index=False)

s3_train_path = sess.upload_data('iris.csv', bucket=bucket, key_prefix=prefix + '/train')

sklearn_estimator = SKLearn(
    entry_point='train.py',
    role=role,
    instance_type='ml.m5.large',
    instance_count=1,
    framework_version='1.0-1',
    py_version='py3',
    base_job_name='sklearn-iris'
)

sklearn_estimator.fit({'train': f's3://{bucket}/{prefix}/train/'})
endpoint_name = 'sklearn-iris-endpoint'
predictor = sklearn_estimator.deploy(1, 'ml.t2.medium', endpoint_name=endpoint_name)
```

Test:

``` python
from sagemaker.serializers import CSVSerializer
from sagemaker.deserializers import JSONDeserializer

predictor.serializer = CSVSerializer()
predictor.deserializer = JSONDeserializer()
print(predictor.predict('5.1,3.5,1.4,0.2'))
```

------------------------------------------------------------------------

## Step 6B --- Run Locally (outside Studio)

Replace `get_execution_role()` with your role ARN.

------------------------------------------------------------------------

## Step 7 --- Logs

Training logs in **CloudWatch Logs**: `/aws/sagemaker/TrainingJobs`.

------------------------------------------------------------------------

## Step 8 --- CLI Prediction

``` bash
aws sagemaker-runtime invoke-endpoint   --endpoint-name sklearn-iris-endpoint   --body "5.1,3.5,1.4,0.2"   --content-type "text/csv"   output.json
cat output.json
```

------------------------------------------------------------------------

## Step 9 --- Cleanup

``` bash
aws sagemaker delete-endpoint --endpoint-name sklearn-iris-endpoint
aws sagemaker delete-endpoint-config --endpoint-config-name sklearn-iris-endpoint
aws sagemaker delete-model --model-name <model-name>
aws s3 rm s3://my-sagemaker-bucket-<unique>/sagemaker/iris-example --recursive
```

Detach IAM role policies if created just for demo:

``` bash
aws iam detach-role-policy --role-name MySageMakerRole --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
aws iam detach-role-policy --role-name MySageMakerRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
aws iam delete-role --role-name MySageMakerRole
```

------------------------------------------------------------------------

## Notes

-   Delete endpoints after testing to avoid charges.
-   Use small instance types for demos (`ml.m5.large`, `ml.t2.medium`).
-   Keep your S3 clean.
