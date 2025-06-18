# embed_and_store_chunks.py

from tools import load_and_chunk_pdf
from bedrock_wrapper import embed_texts
import os
import json
import numpy as np
import faiss
import boto3
from dotenv import load_dotenv
from pathlib import Path
from typing import List, Dict, Any, Tuple

# Load environment variables
load_dotenv()

# Get bucket name from environment
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
if not S3_BUCKET:
    raise ValueError("Please set S3_BUCKET_NAME environment variable")

# Cache file paths
CACHE_DIR = Path("cache")
EMBEDDINGS_FILE = CACHE_DIR / "embeddings.npy"
CHUNKS_FILE = CACHE_DIR / "chunks.json"
FAISS_INDEX_FILE = CACHE_DIR / "faiss_index.bin"
PROCESSED_FILES_LIST = CACHE_DIR / "processed_files.json"

def get_s3_pdf_keys() -> List[str]:
    """Get list of PDF files from S3 bucket."""
    s3 = boto3.client('s3')
    response = s3.list_objects_v2(Bucket=S3_BUCKET)
    pdf_keys = []
    
    if 'Contents' in response:
        for obj in response['Contents']:
            if obj['Key'].lower().endswith('.pdf'):
                pdf_keys.append(obj['Key'])
    
    return pdf_keys

def get_processed_files() -> List[str]:
    """Get list of already processed files from cache."""
    if not PROCESSED_FILES_LIST.exists():
        return []
    
    with open(PROCESSED_FILES_LIST, 'r') as f:
        return json.load(f)

def save_to_cache(chunks: List[Dict[str, Any]], embeddings: np.ndarray, processed_files: List[str]):
    """Save chunks, embeddings, and processed files list to cache."""
    # Create cache directory if it doesn't exist
    CACHE_DIR.mkdir(exist_ok=True)
    
    if len(chunks) > 0 and embeddings is not None and embeddings.size > 0:
        # Save embeddings as numpy array
        np.save(EMBEDDINGS_FILE, embeddings)
        
        # Save chunks as JSON
        with open(CHUNKS_FILE, "w") as f:
            json.dump(chunks, f)
        
        # Create and save FAISS index
        dimension = embeddings.shape[1]  # Get embedding dimension
        index = faiss.IndexFlatL2(dimension)  # Create FAISS index
        index.add(embeddings.astype('float32'))  # Add vectors to index
        faiss.write_index(index, str(FAISS_INDEX_FILE))
    
    # Save list of processed files
    with open(PROCESSED_FILES_LIST, 'w') as f:
        json.dump(processed_files, f)
    
    print(f"✅ Cache updated with {len(chunks)} total chunks from {len(processed_files)} documents")

def load_from_cache() -> Tuple[List[Dict[str, Any]], np.ndarray]:
    """Load chunks and embeddings from cache if they exist."""
    if not (EMBEDDINGS_FILE.exists() and CHUNKS_FILE.exists() and FAISS_INDEX_FILE.exists()):
        return [], np.array([])
        
    try:
        embeddings = np.load(EMBEDDINGS_FILE)
        with open(CHUNKS_FILE, 'r') as f:
            chunks = json.load(f)
        print(f"✅ Loaded {len(chunks)} existing chunks from cache")
        return chunks, embeddings
    except Exception as e:
        print(f"❌ Error loading from cache: {str(e)}")
        return [], np.array([])

def process_documents():
    # Get current PDFs in S3
    pdf_keys = get_s3_pdf_keys()
    print(f"📚 Found {len(pdf_keys)} PDF files in S3")
    
    # Get list of already processed files
    processed_files = get_processed_files()
    print(f"📝 Found {len(processed_files)} previously processed files")
    
    # Identify new files to process
    new_files = [key for key in pdf_keys if key not in processed_files]
    print(f"🆕 Found {len(new_files)} new files to process")
    
    # Load existing chunks and embeddings
    all_chunks, all_embeddings = load_from_cache()
    
    # Convert all_embeddings to list for appending if it's empty
    embeddings_list = [] if len(all_embeddings) == 0 else all_embeddings.tolist()
    
    # Process new files
    for key in new_files:
        print(f"📄 Processing: {key}")
        try:
            # Load and chunk the PDF
            chunks = load_and_chunk_pdf(S3_BUCKET, key)
            texts = [c["text"] for c in chunks]

            # Generate embeddings for the chunks
            new_embeddings = embed_texts(texts)
            
            # Store results
            all_chunks.extend(chunks)
            embeddings_list.extend(new_embeddings)
            processed_files.append(key)
            
            print(f"✅ Processed {len(chunks)} chunks from {key}")
            
        except Exception as e:
            print(f"❌ Error processing {key}: {str(e)}")
            continue

    # Convert embeddings list back to numpy array
    final_embeddings = np.array(embeddings_list) if embeddings_list else np.array([])
    
    # Save updated cache
    save_to_cache(all_chunks, final_embeddings, processed_files)
    
    return all_chunks, final_embeddings
 
if __name__ == "__main__":
    chunks, embeddings = process_documents()
    
    # Print example of first chunk and its embedding
    if len(chunks) > 0 and embeddings.size > 0:
        print("\nExample chunk:")
        print(f"Text: {chunks[0]['text'][:200]}...")
        print(f"Source: {chunks[0]['source']}")
        print(f"Chunk ID: {chunks[0]['chunk_id']}")
        print(f"Embedding (first 5 dimensions): {embeddings[0][:5]}...") 
