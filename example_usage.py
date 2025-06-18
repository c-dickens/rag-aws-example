from typing import List, Dict, Any
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.agents import initialize_agent, AgentType
from vector_retriever import VectorRetriever
from bedrock_wrapper import get_bedrock_llm

def demo_rag():
    """Demonstrate RAG capabilities."""
    print("\n=== RAG Demo ===")
    
    try:
        # Create retriever
        retriever = VectorRetriever()
        
        # Example query
        query = "What are the FDA's guidelines for AI in medical devices?"
        print(f"\nQuestion: {query}")
        
        # Get relevant chunks
        chunks = retriever.retrieve(query, k=3)
        
        # Format chunks for display
        for i, chunk in enumerate(chunks, 1):
            print(f"\nRelevant Chunk {i}:")
            print(f"Source: {chunk['source']}")
            print(f"Text: {chunk['text'][:200]}...")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        raise

if __name__ == "__main__":
    demo_rag() 