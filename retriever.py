import numpy as np
import faiss
import json
from pathlib import Path
from typing import List, Dict, Any
from bedrock_wrapper import embed_texts

class RAGRetriever:
    def __init__(self, index_path: str = "cache/faiss_index.bin", chunks_path: str = "cache/chunks.json"):
        """Initialize the RAG retriever with FAISS index and chunks."""
        self.index_path = Path(index_path)
        self.chunks_path = Path(chunks_path)
        self.index = None
        self.chunks = None
        self._load_or_initialize()
    
    def _load_or_initialize(self):
        """Load existing index and chunks or initialize new ones."""
        if self.index_path.exists() and self.chunks_path.exists():
            # Load existing index and chunks
            self.index = faiss.read_index(str(self.index_path))
            with open(self.chunks_path, 'r') as f:
                self.chunks = json.load(f)
            print(f"✅ Loaded existing index with {self.index.ntotal} vectors")
        else:
            raise ValueError("Index and chunks not found. Please run embed_and_store_chunks.py first.")
    
    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Retrieve the top-k most relevant chunks for a query.
        
        Args:
            query (str): The query text
            k (int): Number of chunks to retrieve
            
        Returns:
            List[Dict[str, Any]]: List of retrieved chunks with their metadata
        """
        # Embed the query
        query_embedding = embed_texts(query)
        
        # Convert to numpy array and reshape for FAISS
        query_vector = np.array([query_embedding]).astype('float32')
        
        # Search the index
        distances, indices = self.index.search(query_vector, k)
        
        # Get the corresponding chunks
        retrieved_chunks = [self.chunks[idx] for idx in indices[0]]
        
        return retrieved_chunks 
