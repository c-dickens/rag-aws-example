from bedrock_wrapper import embed_texts, generate_answer

def test_embedding():
    embedding = embed_texts("AI is transforming healthcare.")
    assert isinstance(embedding, list) or isinstance(embedding, (list, float)), "Embedding should be a list or float"
    print("Embedding (truncated):", embedding[:5], "...")

def test_generation():
    context = ["AI can help doctors analyze medical images and patient data to improve diagnostics."]
    response = generate_answer("Explain how AI helps with diagnostics in healthcare.", context)
    assert isinstance(response, str) and len(response) > 0, "Response should be a non-empty string"
    print("Answer:\n", response)
