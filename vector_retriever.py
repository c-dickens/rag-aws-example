from __future__ import annotations

import json
from pathlib import Path
from typing import List, Dict, Any

from langchain.embeddings import BedrockEmbeddings
from langchain.vectorstores import FAISS


class VectorRetriever:
    """LangChain based vector retriever."""

    def __init__(self, index_path: str = "cache/faiss_index.bin", chunks_path: str = "cache/chunks.json"):
        self.index_path = Path(index_path)
        self.chunks_path = Path(chunks_path)
        if not self.index_path.exists() or not self.chunks_path.exists():
            raise ValueError("Index and chunks not found. Run embed_and_store_chunks.py first")

        self.embeddings = BedrockEmbeddings(model_id="amazon.titan-embed-text-v2:0")
        self.store = FAISS.load_local(str(self.index_path), self.embeddings)
        with self.chunks_path.open() as f:
            self.chunks: List[Dict[str, Any]] = json.load(f)

    def retrieve(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """Return top-k chunks for query."""
        docs = self.store.similarity_search(query, k=k)
        results: List[Dict[str, Any]] = []
        for d in docs:
            idx = d.metadata.get("idx")
            meta = self.chunks[idx] if idx is not None and idx < len(self.chunks) else {}
            results.append({"text": d.page_content, **meta})
        return results

    def as_langchain_tool(self, name: str = "search_docs", description: str = "Search cached documents"):
        from langchain.agents import Tool

        def _run(q: str) -> str:
            chunks = self.retrieve(q, k=3)
            return "\n".join(chunk["text"] for chunk in chunks)

        return Tool(name=name, func=_run, description=description)
