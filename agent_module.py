from __future__ import annotations

from langchain.agents import initialize_agent, AgentType
from langchain.llms import Bedrock

from vector_retriever import VectorRetriever
from tool_modules import tool_list


def create_agent():
    """Initialize a LangChain ReAct agent with tools and retriever."""
    llm = Bedrock(model_id="amazon.titan-text-express-v1")
    retriever = VectorRetriever()
    retrieval_tool = retriever.as_langchain_tool(name="search_docs", description="Search cached documents")

    tools = [retrieval_tool] + tool_list()

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.REACT_DESCRIPTION,
        verbose=True,
    )
    return agent
