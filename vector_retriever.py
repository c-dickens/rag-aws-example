from __future__ import annotations

import json
import pickle
import faiss
import numpy as np
from pathlib import Path
from typing import List, Dict, Any

from langchain_aws import BedrockEmbeddings


class VectorRetriever:
    """Custom vector retriever using pre-computed embeddings."""

    def __init__(self, cache_dir: str = "cache"):
        """Initialize retriever with cache directory.
        
        Args:
            cache_dir: Directory containing the FAISS index and docstore
        """
        self.cache_dir = Path(cache_dir)
        
        # Load FAISS index
        index_path = self.cache_dir / "index.faiss"
        if not index_path.exists():
            raise ValueError("FAISS index not found. Run embed_and_store_chunks.py first")
        self.index = faiss.read_index(str(index_path))
        
        # Load docstore
        docstore_path = self.cache_dir / "docstore.pkl"
        if not docstore_path.exists():
            raise ValueError("Docstore not found. Run embed_and_store_chunks.py first")
        with open(docstore_path, "rb") as f:
            docstore_data = pickle.load(f)
            self.docstore = docstore_data["docstore"]
            self.index_to_docstore_id = docstore_data["index_to_docstore_id"]
        
        # Initialize embeddings model for queries
        self.embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Return top-k chunks for query."""
        # Get query embedding
        query_embedding = self.embeddings.embed_query(query)
        
        # Search FAISS index
        D, I = self.index.search(np.array([query_embedding], dtype=np.float32), k)
        
        # Get documents
        results = []
        for idx in I[0]:
            if idx != -1:  # FAISS returns -1 if not enough results
                doc = self.docstore[self.index_to_docstore_id[idx]]
                results.append({
                    "text": doc.page_content,
                    "source": doc.metadata.get("source"),
                    "chunk_id": doc.metadata.get("chunk_id"),
                    "score": float(D[0][len(results)])
                })
        return results

    def as_langchain_tool(self, name: str = "search_docs", description: str = "Search cached documents"):
        from langchain.agents import Tool

        def _run(q: str) -> str:
            chunks = self.retrieve(q, k=3)
            return "\n".join(f"[Score: {c['score']:.3f}] {c['text']}" for c in chunks)

        return Tool(name=name, func=_run, description=description)
