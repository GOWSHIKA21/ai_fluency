from config import client, MODEL
from tools import get_course_fee, calculator


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_course_fee",
            "description": "Get the fee of a course using its course code.",
            "parameters": {
                "type": "object",
                "properties": {
                    "course_code": {
                        "type": "string",
                        "description": "Course code such as CS101, AI202 or DS303"
                    }
                },
                "required": ["course_code"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Calculate a mathematical expression.",
            "parameters": {
                "type": "object",
                "properties": {
                    "expression": {
                        "type": "string",
                        "description": "Mathematical expression to calculate"
                    }
                },
                "required": ["expression"]
            }
        }
    }
]


def run_tool(name, arguments):
    if name == "get_course_fee":
        return get_course_fee(arguments["course_code"])

    if name == "calculator":
        return calculator(arguments["expression"])

    return "Unknown tool"


def agent(question, max_steps=8):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a ReAct agent. Solve the user's question using the "
                "available tools. Use tools whenever information or arithmetic "
                "is required. Do not invent course fees."
            )
        },
        {
            "role": "user",
            "content": question
        }
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0
        )

        message = response.choices[0].message

        if not message.tool_calls:

            return message.content.strip()

        messages.append(message)

        for tool_call in message.tool_calls:

            name = tool_call.function.name

            import json
            arguments = json.loads(tool_call.function.arguments)

            result = run_tool(name, arguments)

            print(
                f"step {step}: "
                f"{name}({arguments}) -> {result}"
            )

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return "Stopped: maximum steps reached"