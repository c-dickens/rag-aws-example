from typing import List, Dict, Any
from bedrock_wrapper import embed_texts, generate_answer
from retriever import RAGRetriever

def generate_answer_with_rag(query: str, k: int = 3) -> Dict[str, Any]:
    """
    Generate an answer using RAG (Retrieval-Augmented Generation).
    
    Args:
        query (str): The user's question
        k (int): Number of chunks to retrieve
        
    Returns:
        Dict[str, Any]: Dictionary containing the answer and sources
    """
    # Initialize retriever
    retriever = RAGRetriever()
    
    # Retrieve relevant chunks
    chunks = retriever.retrieve(query, k)
    
    # Prepare context chunks
    context_chunks = [chunk["text"] for chunk in chunks]
    
    # Generate answer using new signature
    answer = generate_answer(query, context_chunks)
    
    # Get sources
    sources = list(set(chunk["source"] for chunk in chunks))
    
    return {
        "answer": answer,
        "sources": sources
    }

if __name__ == "__main__":
    # Example usage
    query = "Tell me about the FDA's regulation of AI enhanced medical devices or products"
    result = generate_answer_with_rag(query)
    
    print("\nQuestion:", query)
    print("\nAnswer:", result["answer"])
    print("\nSources:", result["sources"]) 