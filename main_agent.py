from agent_module import create_agent

agent = create_agent()


def run_query(query: str) -> str:
    return agent.run(query)


if __name__ == "__main__":
    import sys

    q = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Hello"
    print(run_query(q))
