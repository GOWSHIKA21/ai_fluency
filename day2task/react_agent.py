import json

from config import client, MODEL, banner
from tools import get_equipment_price, calculator


TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_equipment_price",
            "description": "Get the rental price of college event equipment.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Equipment item such as projector, microphone, or speaker"
                    }
                },
                "required": ["item"]
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

    if name == "get_equipment_price":
        return get_equipment_price(arguments["item"])

    if name == "calculator":
        return calculator(arguments["expression"])

    return "Unknown tool"


def agent(question, max_steps=6):

    messages = [
        {
            "role": "system",
            "content": (
                "You are a ReAct agent. "
                "Solve the user's question using the available tools. "
                "If information is required from a tool, call the appropriate tool. "
                "Do not invent tool results. "
                "After obtaining the required information, give a concise final answer."
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
            arguments = json.loads(tool_call.function.arguments)

            print(f"step {step}:")
            print(f"  Action: {name}({arguments})")

            result = run_tool(name, arguments)

            print(f"  Observation: {result}")

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )

    return "Stopped: maximum steps reached"


if __name__ == "__main__":

    banner("REACT AGENT")

    question = (
        "What is the rental price of the projector for the college event, "
        "and if the total budget is Rs. 50,000 with venue cost Rs. 12,000 "
        "and food cost Rs. 8,000, how much money remains after paying for "
        "the venue, food and projector?"
    )

    print("QUESTION:", question)
    print()
    print("--- REACT TRACE ---")

    answer = agent(question)

    print()
    print("FINAL ANSWER:", answer)