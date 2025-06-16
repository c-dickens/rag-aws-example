import argparse
import sys
from typing import Dict, Any
from fastapi import FastAPI, Query
import uvicorn
from rag_pipeline import generate_answer_with_rag

# Initialize FastAPI app
app = FastAPI(
    title="RAG Research Agent API",
    description="API for querying the RAG Research Agent",
    version="1.0.0"
)

def format_output(result: Dict[str, Any]) -> str:
    """Format the RAG result for CLI output."""
    output = []
    output.append("\nAnswer:")
    output.append(result["answer"])
    output.append("\nSources:")
    for source in result["sources"]:
        output.append(f"- {source}")
    return "\n".join(output)

@app.get("/query")
async def query_endpoint(text: str = Query(..., description="The question to ask")):
    """FastAPI endpoint for querying the RAG system."""
    result = generate_answer_with_rag(text)
    return result

def cli_mode():
    """Run the application in CLI mode."""
    parser = argparse.ArgumentParser(description="RAG Research Agent CLI")
    parser.add_argument("--query", type=str, help="The question to ask")
    parser.add_argument("--top_k", type=int, default=3, help="Number of chunks to retrieve")
    parser.add_argument("--debug", action="store_true", help="Print debug information")
    
    args = parser.parse_args()
    
    if not args.query:
        parser.print_help()
        sys.exit(1)
    
    # Get answer from RAG pipeline
    result = generate_answer_with_rag(args.query, k=args.top_k)
    
    # Print formatted output
    print(format_output(result))
    
    # Print debug info if requested
    if args.debug:
        print("\nDebug Information:")
        print(f"Number of sources retrieved: {len(result['sources'])}")

if __name__ == "__main__":
    # Check if FastAPI mode is requested
    if len(sys.argv) > 1 and sys.argv[1] == "--api":
        # Remove the --api flag
        sys.argv.pop(1)
        # Run FastAPI server
        uvicorn.run(app, host="0.0.0.0", port=8000)
    else:
        # Run in CLI mode
        cli_mode() 
