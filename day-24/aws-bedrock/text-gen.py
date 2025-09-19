import boto3
import json

# Initialize Bedrock client
client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Conversation input
messages = [
    {
        "role": "user",
        "content": [
            {"type": "text", "text": "Hello, Bedrock! 👋"}
        ]
    }
]

# Invoke the model with temperature as top-level
response = client.invoke_model(
    modelId="deepseek.v3-v1:0",
    body=json.dumps({
        "messages": messages,
        "temperature": 1
    }),
    contentType="application/json"
)

# Read and decode response
response_body = response['body'].read().decode("utf-8")
result = json.loads(response_body)

# Print response nicely
print(json.dumps(result, indent=2, ensure_ascii=False))


