from embed_and_store_chunks import process_documents

def lambda_handler(event, context):
    process_documents()
    return {"statusCode": 200}
