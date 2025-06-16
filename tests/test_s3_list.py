import boto3
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


def test_s3_list():
    # Get bucket name from environment
    S3_BUCKET = os.getenv("S3_BUCKET_NAME")
    assert S3_BUCKET, "Please set S3_BUCKET_NAME environment variable"
    # Initialize S3 client
    s3 = boto3.client('s3')

    try:
        # List objects in the bucket
        response = s3.list_objects_v2(Bucket=S3_BUCKET)
        
        assert 'Contents' in response or response.get('KeyCount', 0) == 0, "S3 response should have 'Contents' or be empty"
        
        print(f"\nFiles in bucket {S3_BUCKET}:")
        if 'Contents' in response:
            for obj in response['Contents']:
                print(f" - {obj['Key']}")
        else:
            print("No files found in bucket")
        
    except Exception as e:
        print(f"Error listing bucket contents: {str(e)}")
