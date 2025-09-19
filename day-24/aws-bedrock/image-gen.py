import boto3
import json
import base64

# Initialize Bedrock client
client = boto3.client("bedrock-runtime", region_name="ap-south-1")

# Input payload for text-to-image
body = {
    "textToImageParams": {
        "text": "A futuristic city skyline at sunset"
    },
    "taskType": "TEXT_IMAGE",
    "imageGenerationConfig": {
        "cfgScale": 8,
        "seed": 0,
        "width": 1024,
        "height": 1024,
        "numberOfImages": 3
    }
}

# Invoke the model
response = client.invoke_model(
    modelId="amazon.titan-image-generator-v1",
    body=json.dumps(body),
    contentType="application/json",
    accept="application/json"
)

# Read and decode response
response_body = response['body'].read().decode("utf-8")
result = json.loads(response_body)

# The model usually returns a list of base64 strings under 'images'
images_base64 = result.get("images", [])

# Save each image to a PNG file
for idx, image_base64 in enumerate(images_base64):
    image_bytes = base64.b64decode(image_base64)
    with open(f"generated_image_{idx+1}.png", "wb") as f:
        f.write(image_bytes)

print(f"Generated {len(images_base64)} images successfully!")

