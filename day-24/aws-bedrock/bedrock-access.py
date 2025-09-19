import boto3

# Use the "bedrock" client, not "bedrock-runtime"
client = boto3.client("bedrock", region_name="us-east-1")

response = client.list_models()
print("Available Bedrock Models:")
for model in response['modelSummaries']:
    print(model['modelId'])

'''
aws bedrock list-foundation-models --region ap-south-1

'''