# embed_and_store_chunks.py

from tools import load_and_chunk_pdf
from bedrock_wrapper import embed_texts
import os
import json
import numpy as np
import faiss
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

# Get bucket name from environment
S3_BUCKET = os.getenv("S3_BUCKET_NAME")
if not S3_BUCKET:
    raise ValueError("Please set S3_BUCKET_NAME environment variable")

# List of PDF files to process - using actual filenames from S3
PDF_KEYS = [
    "AdvaMed-AI-White-Paper-Final.pdf",
    "isqua-white-paper-on-patient-safety-in-healthcare-organisations.pdf",
    "mhs-iv-patient-safety-practices-year-2.pdf"
]

# Cache file paths
CACHE_DIR = Path("cache")
EMBEDDINGS_FILE = CACHE_DIR / "embeddings.npy"
CHUNKS_FILE = CACHE_DIR / "chunks.json"
FAISS_INDEX_FILE = CACHE_DIR / "faiss_index.bin"

def save_to_cache(chunks, embeddings):
    """Save chunks, embeddings, and FAISS index to cache files."""
    # Create cache directory if it doesn't exist
    CACHE_DIR.mkdir(exist_ok=True)
    
    # Save embeddings as numpy array
    np.save(EMBEDDINGS_FILE, embeddings)
    
    # Save chunks as JSON
    with open(CHUNKS_FILE, "w") as f:
        json.dump(chunks, f)
    
    # Create and save FAISS index
    dimension = len(embeddings[0])  # Get embedding dimension
    index = faiss.IndexFlatL2(dimension)  # Create FAISS index
    index.add(np.array(embeddings).astype('float32'))  # Add vectors to index
    faiss.write_index(index, str(FAISS_INDEX_FILE))  # Save index
    
    print(f"✅ Saved {len(chunks)} chunks, embeddings, and FAISS index to cache")

def load_from_cache():
    """Load chunks, embeddings, and FAISS index from cache if they exist."""
    if not (EMBEDDINGS_FILE.exists() and CHUNKS_FILE.exists() and FAISS_INDEX_FILE.exists()):
        return None, None
        
    try:
        embeddings = np.load(EMBEDDINGS_FILE)
        with open(CHUNKS_FILE, "r") as f:
            chunks = json.load(f)
        print(f"✅ Loaded {len(chunks)} chunks, embeddings, and FAISS index from cache")
        return chunks, embeddings
    except Exception as e:
        print(f"❌ Error loading from cache: {str(e)}")
        return None, None

def process_documents():
    # Try to load from cache first
    chunks, embeddings = load_from_cache()
    if chunks is not None and embeddings is not None:
        return chunks, embeddings

    all_chunks = []
    all_embeddings = []

    for key in PDF_KEYS:
        print(f"📄 Processing: {key}")
        try:
            # Load and chunk the PDF
            chunks = load_and_chunk_pdf(S3_BUCKET, key)
            texts = [c["text"] for c in chunks]

            # Generate embeddings for the chunks
            embeddings = embed_texts(texts)
            
            # Store results
            all_chunks.extend(chunks)
            all_embeddings.extend(embeddings)
            
            print(f"✅ Processed {len(chunks)} chunks from {key}")
            
        except Exception as e:
            print(f"❌ Error processing {key}: {str(e)}")
            continue

    print(f"\n✅ Finished embedding {len(all_chunks)} chunks total.")
    
    # Save to cache
    save_to_cache(all_chunks, all_embeddings)
    
    return all_chunks, all_embeddings
 
if __name__ == "__main__":
    chunks, embeddings = process_documents()
    
    # Print example of first chunk and its embedding
    if len(chunks) > 0 and len(embeddings) > 0:
        print("\nExample chunk:")
        print(f"Text: {chunks[0]['text'][:200]}...")
        print(f"Source: {chunks[0]['source']}")
        print(f"Chunk ID: {chunks[0]['chunk_id']}")
        print(f"Embedding (first 5 dimensions): {embeddings[0][:5]}...") 
