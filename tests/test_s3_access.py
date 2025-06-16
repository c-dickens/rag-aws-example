from dotenv import load_dotenv
import os
import boto3

# Load AWS credentials from .env file
load_dotenv()

# Read values (for confirmation)
print("Access Key ID:", os.getenv("AWS_ACCESS_KEY_ID"))
print("Region:", os.getenv("AWS_DEFAULT_REGION"))

# Initialize the S3 client
s3 = boto3.client('s3')

# Your bucket name (update if different)
bucket_name = os.getenv("S3_BUCKET_NAME")
print(f"Accessing bucket: {bucket_name}")

try:
    # List files in the bucket
    response = s3.list_objects_v2(Bucket=bucket_name)
    print(f"\n✅ Successfully connected to bucket: {bucket_name}")
    
    print("Files in bucket:")
    for obj in response.get('Contents', []):
        print(" -", obj['Key'])

except Exception as e:
    print("\n❌ Error accessing S3:")
    print(e)
