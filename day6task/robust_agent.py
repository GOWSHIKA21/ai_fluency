"""Day 6: Robust college canteen agent."""

import json
import sys
from pathlib import Path

sys.path.append(
    str(Path(__file__).parent.parent / "day1")
)

from config import client, MODEL, banner
from tools_v2 import TOOLS, TOOL_FUNCTIONS, SCHEMAS
from validate import validate_arguments


SYSTEM_PROMPT = """
You are a college canteen assistant.

You can:
1. Get the price of a food item.
2. Check whether a food item is available.

Never guess food prices or availability.
Always use the appropriate tool.

Valid food items:
dosa, idli, fried_rice, noodles, coffee.

If the user asks about price, use get_food_price.
If the user asks about availability, use check_availability.

If the user asks about both price and availability,
call both tools.

If no tool is required, answer directly.
"""


MAX_TOKENS = 300
REPEAT_LIMIT = 3


def handle_tool_call(call, log=True):

    name = call.function.name
    raw = call.function.arguments or "{}"


    # =====================================================
    # STAGE 1: PARSE JSON
    # =====================================================

    try:

        arguments = json.loads(raw)

    except json.JSONDecodeError as error:

        result = (
            f"Argument error: invalid JSON ({error}). "
            f"Send valid JSON for '{name}'."
        )

        if log:
            print("      INVALID JSON")
            print("      ", result)

        return result


    # =====================================================
    # STAGE 2: LOOK UP TOOL
    # =====================================================

    function = TOOL_FUNCTIONS.get(name)

    if function is None:

        result = (
            f"Unknown tool: {name}. "
            f"Available tools: {', '.join(TOOL_FUNCTIONS)}."
        )

        if log:
            print("      UNKNOWN TOOL")
            print("      ", result)

        return result


    # =====================================================
    # STAGE 3: VALIDATE ARGUMENTS
    # =====================================================

    problem = validate_arguments(
        arguments,
        SCHEMAS[name]
    )

    if problem:

        result = f"Argument error: {problem}"

        if log:
            print("      VALIDATION ERROR")
            print("      ", result)

        return result


    # =====================================================
    # STAGE 4: EXECUTE TOOL
    # =====================================================

    try:

        result = str(
            function(**arguments)
        )

    except Exception as error:

        result = (
            f"Tool error in {name}: "
            f"{type(error).__name__}: {error}"
        )

        if log:
            print("      TOOL EXECUTION ERROR")
            print("      ", result)

        return result


    if log:

        print(
            f"      {name}({arguments}) -> {result}"
        )

    return result


def agent(question, max_steps=6, verbose=True):

    messages = [
        {
            "role": "system",
            "content": SYSTEM_PROMPT
        },
        {
            "role": "user",
            "content": question
        }
    ]

    seen = {}

    max_tokens = MAX_TOKENS

    for step in range(1, max_steps + 1):

        response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
            tools=TOOLS,
            temperature=0,
            max_tokens=max_tokens
        )

        choice = response.choices[0]
        message = choice.message


        # =================================================
        # FINISH_REASON = LENGTH
        # =================================================

        if choice.finish_reason == "length":

            if max_tokens >= 2000:

                return (
                    "Stopped: reply remained truncated "
                    "at 2000 tokens."
                )

            max_tokens *= 2

            if verbose:

                print(
                    f"step {step}: truncated, "
                    f"retrying with max_tokens={max_tokens}"
                )

            continue


        # =================================================
        # FINAL ANSWER
        # =================================================

        if not message.tool_calls:

            return (
                message.content or ""
            ).strip()


        # =================================================
        # ASSISTANT TOOL CALL MESSAGE
        # =================================================

        messages.append(
            {
                "role": "assistant",
                "content": message.content or "",
                "tool_calls": [
                    {
                        "id": call.id,
                        "type": "function",
                        "function": {
                            "name": call.function.name,
                            "arguments": call.function.arguments
                        }
                    }
                    for call in message.tool_calls
                ]
            }
        )


        if verbose:

            print(
                f"step {step}: "
                f"{len(message.tool_calls)} tool call(s)"
            )


        # =================================================
        # HANDLE ALL TOOL CALLS
        # =================================================

        for call in message.tool_calls:

            signature = (
                call.function.name,
                call.function.arguments
            )

            seen[signature] = (
                seen.get(signature, 0) + 1
            )


            # =============================================
            # REPEATED IDENTICAL CALL
            # =============================================

            if seen[signature] >= REPEAT_LIMIT:

                return (
                    f"Stopped: {call.function.name} "
                    f"was called {REPEAT_LIMIT} times "
                    f"with the same arguments."
                )


            result = handle_tool_call(
                call,
                log=verbose
            )


            # =============================================
            # SEND RESULT BACK TO MODEL
            # =============================================

            messages.append(
                {
                    "role": "tool",
                    "tool_call_id": call.id,
                    "content": result
                }
            )


    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


# =========================================================
# TEST QUESTIONS
# =========================================================

if __name__ == "__main__":

    banner("DAY 6 - ROBUST CANTEEN AGENT")

    questions = [

        # 1. SINGLE TOOL
        "What is the price of dosa?",

        # 2. PARALLEL TOOL CALL
        "Tell me the price and availability of dosa.",

        # 3. INVALID VALUE
        "What is the price of pizza?",

        # 4. NO TOOL
        "Write a one-line welcome message for new students."

    ]


    for question in questions:

        print("\n" + "=" * 70)

        print("Q:", question)

        print("=" * 70)

        answer = agent(question)

        print("A:", answer)