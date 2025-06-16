from dotenv import load_dotenv
import os
import boto3

# Load AWS credentials from .env file
load_dotenv()

def test_s3_access():
    # Read values (for confirmation)
    access_key = os.getenv("AWS_ACCESS_KEY_ID")
    region = os.getenv("AWS_DEFAULT_REGION")
    bucket_name = os.getenv("S3_BUCKET_NAME")
    assert access_key, "AWS_ACCESS_KEY_ID must be set"
    assert region, "AWS_DEFAULT_REGION must be set"
    assert bucket_name, "S3_BUCKET_NAME must be set"
    print("Access Key ID:", access_key)
    print("Region:", region)
    print(f"Accessing bucket: {bucket_name}")
    # Initialize the S3 client
    s3 = boto3.client('s3')
    try:
        # List files in the bucket
        response = s3.list_objects_v2(Bucket=bucket_name)
        print(f"\n✅ Successfully connected to bucket: {bucket_name}")
        print("Files in bucket:")
        for obj in response.get('Contents', []):
            print(" -", obj['Key'])
        # Assert that the response is a dict and has expected keys
        assert isinstance(response, dict), "S3 response should be a dict"
        assert 'ResponseMetadata' in response, "S3 response should have 'ResponseMetadata'"
    except Exception as e:
        print("\n❌ Error accessing S3:")
        print(e)
        assert False, f"Exception occurred: {e}"
