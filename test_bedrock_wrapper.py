from bedrock_wrapper import embed_texts, generate_answer

# ✅ Test Embedding
embedding = embed_texts("AI is transforming healthcare.")
print("Embedding (truncated):", embedding[:5], "...")

# ✅ Test Generation
response = generate_answer("Explain how AI helps with diagnostics in healthcare.")
print("Answer:\n", response)
