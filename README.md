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
- `test_*.py`: Test files for various components
- `docs/`: Documentation
- `notebooks/`: Jupyter notebooks for experimentation

## Testing

Run the test suite:
```bash
python -m pytest test_*.py
```

## License

MIT License 