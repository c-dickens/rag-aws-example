from agent_module import create_agent

agent = create_agent()

def lambda_handler(event, context):
    query = event.get("query", "")
    if not query:
        return {"statusCode": 400, "body": "Missing query"}
    response = agent.run(query)
    return {"statusCode": 200, "body": response}
