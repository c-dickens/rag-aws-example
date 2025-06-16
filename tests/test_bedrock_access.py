import boto3
import os
from dotenv import load_dotenv

load_dotenv()

def test_bedrock_access():
    # Use bedrock client for listing models
    client = boto3.client("bedrock", region_name=os.getenv("AWS_DEFAULT_REGION"))
    response = client.list_foundation_models()
    assert "modelSummaries" in response, "Response should contain 'modelSummaries'"
    print("✅ Connected to Bedrock! Models available:")
    for model in response["modelSummaries"]:
        print(f"- {model['modelId']} ({model['providerName']})")
