# bedrock_wrapper.py

import boto3
import json
import os
from dotenv import load_dotenv

load_dotenv()

def get_bedrock_client():
    return boto3.client("bedrock-runtime", region_name=os.getenv("AWS_DEFAULT_REGION"))


def embed_texts(text_list, model_id="amazon.titan-embed-text-v2:0"):
    """Embeds a list of texts using Titan embedding model."""
    if isinstance(text_list, str):
        text_list = [text_list]

    client = get_bedrock_client()
    
    # Process each text individually
    embeddings = []
    for text in text_list:
        body = {
            "inputText": text
        }
        
        response = client.invoke_model(
            modelId=model_id,
            contentType="application/json",
            accept="application/json",
            body=json.dumps(body)
        )
        
        result = json.loads(response["body"].read())
        embeddings.append(result["embedding"])
    
    return embeddings[0] if len(text_list) == 1 else embeddings


def generate_answer(prompt, context_chunks, model_id="amazon.titan-text-express-v1"):
    """Generates a response to a prompt and context using Titan model.
    Args:
        prompt (str): The user question
        context_chunks (List[str]): List of context strings
        model_id (str): Model to use (default Titan)
    Returns:
        str: The generated answer
    """
    client = get_bedrock_client()

    # Format the input as specified
    context = "\n\n".join(context_chunks)
    formatted_prompt = f"""System: You are a helpful healthcare assistant.\n\nContext:\n{context}\n\nUser question: {prompt}\n"""

    body = {
        "inputText": formatted_prompt,
        "textGenerationConfig": {
            "maxTokenCount": 512,
            "temperature": 0.7,
            "topP": 1,
            "stopSequences": []
        }
    }

    response = client.invoke_model(
        modelId=model_id,
        contentType="application/json",
        accept="application/json",
        body=json.dumps(body)
    )

    return json.loads(response["body"].read())["results"][0]["outputText"]
