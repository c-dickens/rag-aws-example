# bedrock_wrapper.py

from langchain_aws import BedrockLLM, BedrockEmbeddings
import boto3
import json
import os
from dotenv import load_dotenv
from typing import List, Union

load_dotenv()

def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION"))

def get_bedrock_llm(model_id: str = "amazon.titan-text-express-v1") -> BedrockLLM:
    """Get a LangChain Bedrock LLM instance."""
    return BedrockLLM(
        model_id=model_id,
        client=get_bedrock_client(),
        model_kwargs={
            "maxTokenCount": 512,
            "temperature": 0.7,
            "topP": 1,
            "stopSequences": []
        },
        streaming=True
    )

def embed_texts(text_list: Union[str, List[str]], model_id: str = "amazon.titan-embed-text-v2:0") -> Union[List[float], List[List[float]]]:
    """Embeds texts using Titan embedding model through LangChain."""
    embeddings = BedrockEmbeddings(
        client=get_bedrock_client(),
        model_id=model_id
    )
    
    if isinstance(text_list, str):
        return embeddings.embed_query(text_list)
    return embeddings.embed_documents(text_list)

def generate_answer(prompt: str, context_chunks: List[str], model_id: str = "amazon.titan-text-express-v1") -> str:
    """Generates a response using LangChain's Bedrock integration.
    
    Args:
        prompt (str): The user question
        context_chunks (List[str]): List of context strings
        model_id (str): Model to use (default Titan)
    Returns:
        str: The generated answer
    """
    llm = get_bedrock_llm(model_id)
    
    # Format the input as specified
    context = "\n\n".join(context_chunks)
    formatted_prompt = f"""System: You are a helpful healthcare assistant.

Context:
{context}

User question: {prompt}
"""
    
    return llm.predict(formatted_prompt)
