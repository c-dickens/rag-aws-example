from tools import process_all_pdfs_in_bucket
import os
from dotenv import load_dotenv

load_dotenv()

def test_pdf_processing():
    # Get bucket name from environment variable
    bucket = os.getenv('S3_BUCKET_NAME')
    print(f"Processing bucket: {bucket}")
    if not bucket:
        raise ValueError("Please set S3_BUCKET_NAME environment variable")
    
    # Process all PDFs in the docs/ prefix
    chunks = process_all_pdfs_in_bucket(bucket, prefix='')
    
    # Print summary
    print(f"\nProcessed {len(chunks)} chunks from PDFs in bucket {bucket}")
    
    # Print first chunk as example
    if chunks:
        print("\nExample chunk:")
        print(f"Source: {chunks[0]['source']}")
        print(f"Chunk ID: {chunks[0]['chunk_id']}")
        print(f"Text preview: {chunks[0]['text'][:200]}...")

if __name__ == "__main__":
    test_pdf_processing() 