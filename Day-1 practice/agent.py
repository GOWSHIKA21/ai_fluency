import json
from config import client, MODEL
from tools import TOOLS, get_event_fee, calculate


def run_agent(question):

    messages = [
        {
            "role": "system",
            "content": """
You are a college event registration assistant.

You have access to tools that contain private event information.
Always use the tools when the question requires event fees or calculations.

Available events:
TECHFEST2026
AIWORKSHOP2026
HACKATHON2026

For questions about event fees, use get_event_fee.
For mathematical calculations, use calculate.
Do not guess private event information.
"""
        },
        {
            "role": "user",
            "content": question
        }
    ]

    while True:

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto"
        )

        message = response.choices[0].message

        if not message.tool_calls:
            return message.content

        messages.append(message)

        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)

            print("Tool called:", tool_name)
            print("Arguments:", arguments)

            if tool_name == "get_event_fee":
                result = get_event_fee(arguments["event_name"])

            elif tool_name == "calculate":
                result = calculate(arguments["expression"])

            else:
                result = "Unknown tool"

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result)
                }
            )


if __name__ == "__main__":

    questions = [
        "What is the registration fee for TECHFEST2026?",
        "What is the total cost of TECHFEST2026 and AIWORKSHOP2026 after a 10% discount?",
        "Is TECHFEST2026 more expensive than AIWORKSHOP2026? If yes, by how much?",
        "Give me a two-line welcome message for the college events."
    ]

    for question in questions:
        print("\n" + "=" * 60)
        print("Question:", question)

        answer = run_agent(question)

        print("Final Answer:", answer)