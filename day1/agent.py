from config import client, MODEL
from tools import TOOLS, get_course_fee, calculator


SYSTEM_PROMPT = """
You are a college fee assistant.

Rules:
1. Never guess a course fee. Always use get_course_fee.
2. Use calculator for arithmetic.
3. Available course codes: CS101, AI202, DS303.
4. If no tool is needed, answer directly.
"""


def agent(question, max_steps=6):
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            tool_choice="auto",
            temperature=0,
        )

        message = response.choices[0].message

        # If the model gives a normal answer, return it
        if not message.tool_calls:
            return message.content

        # Add the assistant's tool request to the conversation
        messages.append(message)

        # Execute each requested tool
        for tool_call in message.tool_calls:

            tool_name = tool_call.function.name

            # Fix Groq's malformed tool name if it occurs
            if "<|channel|>" in tool_name:
                tool_name = tool_name.split("<|channel|>")[0]

            arguments = tool_call.function.arguments

            import json
            args = json.loads(arguments)

            if tool_name == "get_course_fee":
                result = get_course_fee(**args)

            elif tool_name == "calculator":
                result = calculator(**args)

            else:
                result = f"Unknown tool: {tool_name}"

            print(
                f" step {step}: "
                f"{tool_name}({args}) -> {result}"
            )

            # Send tool result back to the model
            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "content": str(result),
                }
            )

    return "Sorry, I could not complete the request within the step limit."


if __name__ == "__main__":

    questions = [
        "What is the fee for AI202?",

        "What is the total fee for CS101 and AI202 "
        "after a 10% scholarship?",

        "Is DS303 more expensive than CS101, and by how much?",

        "Write a two-line welcome message for new AI students.",
    ]

    print(
        f"\n=== SYSTEM 3: AI AGENT | "
        f"provider: groq | model: {MODEL} ===\n"
    )

    for question in questions:
        print(f"Q: {question}")

        try:
            print("A:", agent(question))
        except Exception as e:
            print("ERROR:", e)

        print("-" * 70)