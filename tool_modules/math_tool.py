from langchain.agents import Tool
import sympy as sp


def solve_math(expression: str) -> str:
    try:
        return str(sp.simplify(expression))
    except Exception as exc:
        return f"Error: {exc}"

math_tool = Tool(
    name="calculator",
    func=solve_math,
    description="Solve math expressions"
)
