# RAG Research Agent

A Python-based Research Agent that uses Retrieval-Augmented Generation (RAG) to process and analyze documents.

## Features

- PDF document processing and chunking
- AWS Bedrock integration for AI/ML capabilities
- S3 storage integration
- Document embedding and vector storage
- Testing suite for core functionality

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure AWS credentials:
- Ensure you have AWS credentials configured with appropriate permissions for Bedrock and S3
- Set up your AWS credentials in `~/.aws/credentials` or using environment variables

## Project Structure

- `bedrock_wrapper.py`: AWS Bedrock integration
- `embed_and_store_chunks.py`: Document processing and embedding
- `tools.py`: Core utility functions
- `tests/`: Directory containing all test files
- `docs/`: Documentation
- `notebooks/`: Jupyter notebooks for experimentation

## Testing

To run all tests:
```bash
python -m pytest tests/
```

To run a specific test file:
```bash
python -m pytest tests/test_rag_pipeline.py
```

For verbose output:
```bash
python -m pytest -v tests/
```

## Bedrock LLM Call Usage

The function `generate_answer(prompt, context_chunks)` in `bedrock_wrapper.py` calls an LLM (Titan) to answer a user question using retrieved context. Example usage:

```python
from bedrock_wrapper import generate_answer

context_chunks = ["Chunk 1 text", "Chunk 2 text"]
user_question = "What are the benefits of AI in healthcare?"
response = generate_answer(user_question, context_chunks)
print(response)
```

## License

MIT License 
