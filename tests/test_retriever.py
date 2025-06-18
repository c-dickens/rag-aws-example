from vector_retriever import VectorRetriever

def main():
    # Initialize retriever
    retriever = VectorRetriever()
    
    # Test query
    query = "What are the key benefits of RAG systems?"
    print(f"\nQuery: {query}\n")
    
    # Get results
    results = retriever.retrieve(query, k=3)
    
    # Print results
    for i, result in enumerate(results, 1):
        print(f"\nResult {i} [Score: {result['score']:.3f}]")
        print(f"Source: {result['source']}")
        print(f"Text: {result['text'][:200]}...")

if __name__ == "__main__":
    main() 