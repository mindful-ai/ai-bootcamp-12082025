# AWS Bedrock Agent Creation Tutorial

This tutorial provides **step-by-step instructions** to create an agent in the AWS Bedrock console.

---

## Step 1: Log in to AWS Console
1. Go to [AWS Management Console](https://aws.amazon.com/console/).
2. Ensure your account has **Bedrock access**.
3. Switch to **us-east-1** region (Bedrock is only available here).

---

## Step 2: Navigate to Amazon Bedrock
1. In the console search bar, type **"Bedrock"** and select **Amazon Bedrock**.
2. You will land on the Bedrock **Dashboard**.

---

## Step 3: Check Available Models
1. Click on **Foundation Models** in the left menu.
2. Note the **model IDs** available to your account:
   - Titan Text G1
   - Titan Text G1 Lite
   - DeepSeek
   - Other partner models
3. Copy the **model ID** you want to use.

---

## Step 4: Create a New Agent
1. In the left menu, click **Agents**.
2. Click **Create Agent**.

### 4a: Configure Agent Basics
- **Name:** e.g., `LegalDocSummarizer`
- **Description:** Optional, e.g., "Summarizes legal documents in plain English."
- **Tags:** Optional, for organizing resources.

### 4b: Choose Foundation Model
- Select the **model ID** you noted earlier.
- Adjust model parameters if available:
  - Max tokens
  - Temperature

### 4c: Set Agent Behavior (Optional)
- Pre-configure instructions like:
  - "Always summarize text in simple language."
  - "Respond in bullet points."
- Optional: configure **tool integrations** for external services.

### 4d: Review & Create
- Review all settings.
- Click **Create Agent**.
- Your agent is now deployed and ready to be invoked.

---

## Step 5: Test the Agent
1. Click your agent in the **Agents** list.
2. In the **Test** panel, input a prompt, e.g.:
```
Summarize the following contract in simple English:
[Paste your text here]
```
3. Click **Run** to see the generated output.

---

## Step 6: Use Agent via SDK or CLI

### Python (boto3) Example
```python
import boto3, json

runtime_client = boto3.client("bedrock-runtime", region_name="us-east-1")

agent_model_id = "<your-agent-model-id>"  # copy from console

prompt = {
    "inputText": "Summarize this legal document in simple English: [paste text here]"
}

response = runtime_client.invoke_model(
    modelId=agent_model_id,
    contentType="application/json",
    accept="application/json",
    body=json.dumps(prompt)
)

result = json.loads(response['body'].read())
print(result)
```

### CLI Example
```bash
aws bedrock-runtime converse \
  --model-id <your-agent-model-id> \
  --region us-east-1 \
  --input-text "Summarize this legal document in simple English"
```

---

## Tips for Best Results
1. Start with **Lite models** for faster testing.
2. Adjust **temperature** for creativity (0.2–0.5 for legal text).
3. For complex workflows, integrate **tools** in your agent later.
4. Use **console testing** first before calling via SDK/CLI.