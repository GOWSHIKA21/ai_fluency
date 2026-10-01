"""Day 3: tools for the agent you build yourself."""

import ast
import operator
import os
import re


# ---------- Tool 1: Safe Calculator ----------

_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
}


def _evaluate(node):
    if isinstance(node, ast.Constant) and isinstance(node.value, (int, float)):
        return node.value

    if isinstance(node, ast.BinOp) and type(node.op) in _OPS:
        left = _evaluate(node.left)
        right = _evaluate(node.right)
        return _OPS[type(node.op)](left, right)

    if isinstance(node, ast.UnaryOp) and type(node.op) in _OPS:
        operand = _evaluate(node.operand)
        return _OPS[type(node.op)](operand)

    raise ValueError("Unsupported expression")


def calculator(expression: str) -> str:
    """Evaluate a basic arithmetic expression."""

    try:
        tree = ast.parse(expression, mode="eval")
        result = _evaluate(tree.body)
        return str(result)

    except Exception as error:
        return f"Calculator error: {error}"


# ---------- Tool 2: Web Page Reader ----------

TAG = re.compile(
    r"<(script|style)[^>]*>.*?</\1>|<[^>]+>",
    re.S | re.I
)

SPACES = re.compile(r"\s+")


def read_webpage(url: str, max_chars: int = 2000) -> str:
    """Fetch a web page or local HTML/text file and return its text."""

    try:

        # Read online webpage
        if url.startswith("http://") or url.startswith("https://"):

            import requests

            response = requests.get(
                url,
                timeout=10,
                headers={
                    "User-Agent": "AgenticAI-Lab/1.0"
                }
            )

            response.raise_for_status()
            raw = response.text

        # Read local file
        elif os.path.exists(url):

            with open(
                url,
                encoding="utf-8",
                errors="ignore"
            ) as file:
                raw = file.read()

        else:
            return f"Read error: '{url}' is not a URL and no such file exists."

    except Exception as error:
        return f"Read error: {type(error).__name__}: {error}"

    # Remove HTML tags
    text = TAG.sub(" ", raw)

    # Remove extra spaces
    text = SPACES.sub(" ", text).strip()

    # Limit output size
    if len(text) > max_chars:
        text = (
            text[:max_chars]
            + f" ... [truncated, {len(text)} characters total]"
        )

    return text or "Read error: the page contained no readable text."


# ---------- Tool Registry ----------

TOOL_FUNCTIONS = {
    "calculator": calculator,
    "read_webpage": read_webpage,
}


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": (
                "Evaluate an arithmetic expression using "
                "+ - * / ** and brackets."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "The arithmetic expression to evaluate"
                    }
                },
                "required": ["expression"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_webpage",
            "description": (
                "Read a web page or a local HTML/text file "
                "and return its visible text."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "url": {
                        "type": "string",
                        "description": "URL or local file name to read"
                    }
                },
                "required": ["url"]
            }
        }
    }
]


# ---------- Test ----------

if __name__ == "__main__":

    print("Calculator Test 1:")
    print(calculator("(12000 + 18000) * 0.9"))

    print("\nCalculator Test 2:")
    print(calculator("2 ** 10"))

    print("\nWebpage Test:")
    print(read_webpage("notice.html")[:200])