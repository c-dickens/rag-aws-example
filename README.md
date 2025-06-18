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

3. Copy `.env.example` to `.env` and fill in your AWS credentials and S3 bucket details:
```bash
cp .env.example .env
```

4. Configure AWS credentials:
- Ensure you have AWS credentials configured with appropriate permissions for Bedrock and S3
- Set up your AWS credentials in `~/.aws/credentials` or using environment variables

## Preprocessing Documents

Before running any queries or the test suite you need to build the local cache
of embedded document chunks. The script `embed_and_store_chunks.py` downloads
the PDF files from your S3 bucket, generates embeddings using Bedrock and saves
them locally.

Ensure the following environment variables are available (they can be defined
in a `.env` file):

- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `AWS_DEFAULT_REGION` *(or `AWS_REGION`)*
- `S3_BUCKET_NAME`

Run the preprocessing step:

```bash
python embed_and_store_chunks.py
```

After it completes you should see these files inside the `cache/` directory:

- `embeddings.npy`
- `chunks.json`
- `faiss_index.bin`

## Project Structure

- `bedrock_wrapper.py`: AWS Bedrock integration
- `embed_and_store_chunks.py`: Document processing and embedding
- `tools.py`: Core utility functions
- `tests/`: Directory containing all test files
- `docs/`: Documentation
- `notebooks/`: Jupyter notebooks for experimentation
- `vector_retriever.py`: LangChain-based vector store retriever
- `agent_module.py`: Creates the ReAct agent wired with tools
- `tool_modules/`: Collection of LangChain tools
- `observability.py`: Logging and CloudWatch metric helpers
- `lambda_query.py`/`lambda_ingest.py`: AWS Lambda entrypoints

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
