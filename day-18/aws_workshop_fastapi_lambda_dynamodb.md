# AWS Workshop Project: FastAPI + Lambda + DynamoDB

## 📌 Scenario

We are building a **Student Registration System**: - A **FastAPI app**
on EC2 (inside your VPC) exposes a REST API `/register`. - The app
writes student details into **DynamoDB**. - A **Lambda function** can
also read from DynamoDB to return student details.

This example demonstrates: - Networking (VPC) - Compute (EC2, Lambda) -
Database (DynamoDB) - API Development (FastAPI)

------------------------------------------------------------------------

## **Step 1: Create a VPC**

1.  Go to **VPC → Create VPC**.\
2.  Choose **VPC and more**.\
3.  CIDR block: `10.0.0.0/16`.\
4.  Create **2 subnets**:
    -   Public Subnet (`10.0.1.0/24`)\
    -   Private Subnet (`10.0.2.0/24`)\
5.  Select **Internet Gateway** for the public subnet.\
6.  Finish creation.

------------------------------------------------------------------------

## **Step 2: Launch EC2 Instance**

1.  Go to **EC2 → Launch Instance**.\
2.  Choose Amazon Linux 2023 (free tier).\
3.  Instance type: `t2.micro`.\
4.  Network → select **your new VPC**, place it in the **public
    subnet**.\
5.  Enable **Auto-assign Public IP**.\
6.  Add a **Security Group**:
    -   Allow SSH (port 22) from your IP.\
    -   Allow HTTP (port 80) and custom port `8000`.\
7.  Launch with a key pair.

------------------------------------------------------------------------

## **Step 3: Install FastAPI on EC2**

SSH into the instance:

``` bash
sudo yum update -y
sudo yum install -y python3-pip git
pip3 install fastapi uvicorn boto3
```

Create `app.py`:

``` python
from fastapi import FastAPI
import boto3

app = FastAPI()
dynamodb = boto3.resource('dynamodb', region_name="us-east-1")
table = dynamodb.Table("Students")

@app.get("/")
def home():
    return {"message": "FastAPI on AWS works!"}

@app.post("/register/{name}")
def register_student(name: str):
    table.put_item(Item={"name": name})
    return {"status": "registered", "name": name}
```

Run the app:

``` bash
uvicorn app:app --host 0.0.0.0 --port 8000
```

Test: `http://<ec2-public-ip>:8000/`

------------------------------------------------------------------------

## **Step 4: Create DynamoDB Table**

1.  Go to **DynamoDB → Create Table**.\
2.  Table name: `Students`.\
3.  Partition key: `name` (String).\
4.  Leave defaults, create table.

------------------------------------------------------------------------

## **Step 5: Create Lambda Function**

1.  Go to **Lambda → Create function**.\
2.  Name: `GetStudents`. Runtime: Python 3.12.\
3.  Permissions: **Create new role with basic Lambda permissions**.

Then go to **IAM → Roles → \[your Lambda role\] → Attach policy**:\
- For simplicity: attach `AmazonDynamoDBFullAccess`.\
- For least privilege: create a custom inline policy:

``` json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:Scan",
        "dynamodb:GetItem",
        "dynamodb:Query"
      ],
      "Resource": "arn:aws:dynamodb:us-east-1:YOUR_AWS_ACCOUNT_ID:table/Students"
    }
  ]
}
```

Function code:

``` python
import boto3

def lambda_handler(event, context):
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table("Students")
    response = table.scan()
    return {"students": response['Items']}
```

Deploy → Test → Lambda should return records.

------------------------------------------------------------------------

## **Step 6: (Optional) Add API Gateway**

1.  Go to **API Gateway → Create API → HTTP API**.\
2.  Integrate with your Lambda function.\
3.  Deploy → copy endpoint URL.

------------------------------------------------------------------------

# ✅ Final Architecture

-   **VPC** with subnets.\
-   **EC2 instance** running FastAPI → `/register` writes to DynamoDB.\
-   **DynamoDB** stores student data.\
-   **Lambda** reads from DynamoDB → optionally exposed via API Gateway.
