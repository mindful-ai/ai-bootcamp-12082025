import boto3
import json

# Initialize Bedrock runtime client
runtime_client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Your legal document text
legal_text = '''Non-Disclosure Agreement (NDA)
This Non-Disclosure Agreement (“Agreement”) is entered into as of the Effective Date by and between Company A, having its principal place of business at [Address], and Company B, having its principal place of business at [Address].
Confidential Information – Both parties agree to maintain the confidentiality of proprietary information disclosed during the course of discussions, negotiations, or business transactions. Confidential information includes, but is not limited to, business plans, financial data, technical specifications, and customer information.
Obligations of Receiving Party – The receiving party shall not disclose any confidential information to third parties and shall take all reasonable measures to protect such information from unauthorized disclosure.
Exclusions – Confidential information does not include information that is publicly available, independently developed by the receiving party, or disclosed under legal obligation.
Term – The obligations of confidentiality shall survive for a period of three (3) years following the termination of this Agreement.
Governing Law – This Agreement shall be governed by and construed in accordance with the laws of the State of New York, without regard to its conflict of law provisions.
IN WITNESS WHEREOF, the parties have executed this Agreement as of the Effective Date.'''

# Prepare messages for the conversational model
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": f"Summarize the following legal document in simple English:\n{legal_text}"}
        ]
    }
]

# Invoke the model
response = runtime_client.invoke_model(
    modelId="deepseek.v3-v1:0",
    contentType="application/json",
    accept="application/json",
    body=json.dumps({
        "messages": messages,
        "temperature": 0.3,
        "max_tokens": 300
    })
)

# Parse and print the result
result = json.loads(response['body'].read())
print(json.dumps(result, indent=2, ensure_ascii=False))

