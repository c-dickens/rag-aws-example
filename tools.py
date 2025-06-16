import boto3
import io
from typing import List, Dict, Any
from pdfminer.high_level import extract_text
from pdfminer.pdfparser import PDFSyntaxError

def load_pdf_from_s3(bucket: str, key: str) -> bytes:
    """
    Load a PDF file from S3 and return its raw bytes.
    
    Args:
        bucket (str): S3 bucket name
        key (str): S3 object key (path to PDF)
        
    Returns:
        bytes: Raw PDF file content
    """
    s3_client = boto3.client('s3')
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except Exception as e:
        raise Exception(f"Error loading PDF from S3: {str(e)}")

def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract text content from PDF bytes.
    
    Args:
        pdf_bytes (bytes): Raw PDF file content
        
    Returns:
        str: Extracted text content
    """
    try:
        return extract_text(io.BytesIO(pdf_bytes))
    except PDFSyntaxError as e:
        raise Exception(f"Error extracting text from PDF: {str(e)}")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 100) -> List[str]:
    """
    Split text into overlapping chunks of specified size.
    
    Args:
        text (str): Input text to chunk
        chunk_size (int): Size of each chunk in characters
        overlap (int): Number of characters to overlap between chunks
        
    Returns:
        List[str]: List of text chunks
    """
    if not text:
        return []
        
    chunks = []
    start = 0
    text_length = len(text)
    
    while start < text_length:
        end = start + chunk_size
        
        # If this is not the first chunk, include the overlap
        if start > 0:
            start = start - overlap
            
        # If we're near the end, just take the rest
        if end >= text_length:
            chunks.append(text[start:])
            break
            
        # Try to find a good breaking point (space or newline)
        while end < text_length and text[end] not in [' ', '\n']:
            end += 1
            
        chunks.append(text[start:end])
        start = end
        
    return chunks

def process_pdf_from_s3(bucket: str, key: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Process a PDF from S3: load, extract text, and chunk it.
    
    Args:
        bucket (str): S3 bucket name
        key (str): S3 object key
        chunk_size (int): Size of each chunk in characters
        overlap (int): Number of characters to overlap between chunks
        
    Returns:
        List[Dict[str, Any]]: List of chunks with metadata
    """
    try:
        # Load PDF from S3
        pdf_bytes = load_pdf_from_s3(bucket, key)
        
        # Extract text
        text = extract_text_from_pdf(pdf_bytes)
        
        # Chunk the text
        chunks = chunk_text(text, chunk_size, overlap)
        
        # Add metadata to each chunk
        chunked_docs = []
        for i, chunk in enumerate(chunks):
            chunked_docs.append({
                'text': chunk,
                'source': key,
                'chunk_id': i,
                'metadata': {
                    'source_type': 'pdf',
                    'bucket': bucket,
                    'key': key
                }
            })
            
        return chunked_docs
        
    except Exception as e:
        raise Exception(f"Error processing PDF {key} from bucket {bucket}: {str(e)}")
    
def load_and_chunk_pdf(bucket: str, key: str, chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Load a PDF from S3, extract its text, and chunk it.
    
    Args:
        bucket (str): S3 bucket name
        key (str): S3 object key
        chunk_size (int): Size of each chunk in words
        overlap (int): Number of words to overlap between chunks
        
    Returns:
        List[Dict[str, Any]]: List of chunks with metadata
    """
    try:
        pdf_bytes = load_pdf_from_s3(bucket, key)
        text = extract_text_from_pdf(pdf_bytes)
        chunks = chunk_text(text, chunk_size, overlap)

        return [
            {
                "text": chunk,
                "source": key,
                "chunk_id": i
            }
            for i, chunk in enumerate(chunks)
        ]
    except Exception as e:
        raise Exception(f"Error processing PDF {key} from bucket {bucket}: {str(e)}")

def process_all_pdfs_in_bucket(bucket: str, prefix: str = '', chunk_size: int = 500, overlap: int = 100) -> List[Dict[str, Any]]:
    """
    Process all PDFs in an S3 bucket with the given prefix.
    
    Args:
        bucket (str): S3 bucket name
        prefix (str): Prefix to filter PDFs (e.g., 'docs/')
        chunk_size (int): Size of each chunk in characters
        overlap (int): Number of characters to overlap between chunks
        
    Returns:
        List[Dict[str, Any]]: List of all chunks from all PDFs
    """
    s3_client = boto3.client('s3')
    all_chunks = []
    print(f"Processing all PDFs in bucket {bucket} with prefix {prefix}")
    try:
        # List all objects in the bucket with the given prefix
        paginator = s3_client.get_paginator('list_objects_v2')
        for page in paginator.paginate(Bucket=bucket, Prefix=prefix):
            if 'Contents' not in page:
                continue
                
            for obj in page['Contents']:
                key = obj['Key']
                if key.lower().endswith('.pdf'):
                    chunks = process_pdf_from_s3(bucket, key, chunk_size, overlap)
                    all_chunks.extend(chunks)
                    
        return all_chunks
        
    except Exception as e:
        raise Exception(f"Error processing PDFs in bucket {bucket}: {str(e)}") 
