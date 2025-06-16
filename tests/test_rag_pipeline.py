from rag_pipeline import generate_answer_with_rag

def test_rag_pipeline():
    """Test the RAG pipeline with a sample healthcare question."""
    # Test query
    query = "Tell me about the FDA's regulation of AI enhanced medical devices or products"
    
    # Get answer
    result = generate_answer_with_rag(query)
    
    # Print results
    print("\nQuestion:", query)
    print("\nAnswer:", result["answer"])
    print("\nSources:", result["sources"])
    
    # Basic assertions
    assert "answer" in result, "Result should contain 'answer' key"
    assert "sources" in result, "Result should contain 'sources' key"
    assert isinstance(result["answer"], str), "Answer should be a string"
    assert isinstance(result["sources"], list), "Sources should be a list"
    assert len(result["sources"]) > 0, "Should have at least one source"

if __name__ == "__main__":
    test_rag_pipeline() 