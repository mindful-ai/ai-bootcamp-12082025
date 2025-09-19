
# 🚀 AWS Bedrock Tutorial with Legal Document Summarizer Project

## 1. 🔎 What is AWS Bedrock?
AWS **Bedrock** is a **fully managed service** that lets you build and scale **generative AI applications** without managing infrastructure or training models from scratch.

It provides access to **Foundation Models (FMs)** from various providers (Anthropic, Cohere, Meta, Stability AI, Amazon’s Titan models, etc.) through an **API**.

---

## 2. 🏗️ Key Features
- Multiple FMs under one API → You can switch between models (Claude, Llama, Titan, etc.) easily.
- Customizations: Fine-tune models with your own data.
- Agents: Bedrock Agents can call APIs, interact with data sources, and chain reasoning steps.
- Fully Serverless: No need to manage infrastructure.
- Security & Governance: AWS IAM for access control, encryption, and compliance.

---

## 3. 🛠️ Getting Started with AWS Bedrock

### Step 1: Enable Bedrock
1. Sign in to **AWS Console**.
2. Go to **Amazon Bedrock** service.
3. Request access to the models you want (e.g., Claude, Titan, Llama).

### Step 2: Use Bedrock via AWS SDK (Python Example)
```python
import boto3, json

client = boto3.client(service_name="bedrock-runtime", region_name="us-east-1")

model_id = "anthropic.claude-v2"

response = client.invoke_model(
    modelId=model_id,
    contentType="application/json",
    accept="application/json",
    body='{"prompt": "Explain quantum computing in simple terms", "max_tokens_to_sample": 200}'
)

result = json.loads(response['body'].read())
print(result['completion'])
```

---

## 4. ⚡ Using AWS Console (No Code)

### Bedrock Playground
- Test **text generation** and **image generation** directly in the console.
- Adjust parameters (temperature, max tokens, top-p).

### Custom Models
- Upload training data to S3.
- Fine-tune foundation models via the console.

### Agents
- Create agents with step-by-step instructions.
- Attach **APIs or Data Sources (Kendra, S3)** for retrieval-augmented workflows.

---

# 🛠️ Project: Legal Document Summarizer with AWS Bedrock Console

## Step 1: Prepare Legal Documents
- Upload contracts/policies to **S3**.

## Step 2: Access Bedrock Playground
- Open Bedrock Console → **Playground → Chat**.
- Test summarization with Claude or Titan model.

## Step 3: Create an Agent
- Go to **Agents → Create Agent**.
- Name: `LegalSummarizerAgent`.
- Instructions:
  ```
  You are a legal assistant. Summarize legal documents clearly, highlighting:
  - Key obligations
  - Risks and penalties
  - Duration
  - Important clauses
  ```

## Step 4: Connect Agent to Data
- Create an **Amazon Kendra index** linked to your S3 bucket.
- Attach Kendra index to the Agent.

## Step 5: Test Agent
- Ask: *"Summarize the Non-Disclosure Agreement in S3."*
- Get structured summaries.

---

# 🌐 Deploying Legal Summarizer as an API

## Step 1: Confirm Agent
- Note **Agent ID** and **Alias ID**.

## Step 2: Create Lambda
```python
import json
import boto3

def lambda_handler(event, context):
    body = json.loads(event["body"])
    user_query = body.get("query", "Summarize the uploaded contract")

    client = boto3.client("bedrock-agent-runtime", region_name="us-east-1")
    agent_id = "YOUR_AGENT_ID"
    alias_id = "YOUR_AGENT_ALIAS_ID"

    response = client.invoke_agent(
        agentId=agent_id,
        agentAliasId=alias_id,
        sessionId="session1",
        inputText=user_query
    )

    output = ""
    for event in response["completion"]:
        if "chunk" in event:
            output += event["chunk"]["bytes"].decode()

    return {
        "statusCode": 200,
        "headers": {"Content-Type": "application/json"},
        "body": json.dumps({"summary": output})
    }
```

## Step 3: API Gateway
- Create HTTP API → Integrate with Lambda.
- Deploy and copy **Invoke URL**.

## Step 4: Test API
```bash
curl -X POST "https://<api-id>.execute-api.us-east-1.amazonaws.com"   -H "Content-Type: application/json"   -d '{"query": "Summarize the NDA"}'
```

Response:
```json
{
  "summary": "This NDA states that Party A must not disclose Party B’s information for 2 years. Penalties apply if breached."
}
```

---

# ✅ End Result
- Summarizer Agent in Bedrock.
- Lambda wrapper for Bedrock calls.
- API Gateway endpoint usable by apps.

Next Step → Build a Streamlit web app that calls this API for interactive use!
