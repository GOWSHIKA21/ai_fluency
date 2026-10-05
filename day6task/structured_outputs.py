"""Day 6: Robust College Canteen Agent."""

import json
import sys
from pathlib import Path


# =========================================================
# IMPORT DAY 1 CONFIG
# =========================================================

sys.path.append(
    str(Path(__file__).parent.parent / "day1")
)

from config import client, MODEL, banner
from tools_v2 import TOOLS, TOOL_FUNCTIONS, SCHEMAS
from validate import validate_arguments


# =========================================================
# SYSTEM PROMPT
# =========================================================

SYSTEM_PROMPT = """
You are a college canteen assistant.

You have two tools:

1. get_food_price
   - Gets the price of a food item.

2. check_availability
   - Checks whether a food item is available.

Never guess a food price or availability.

Valid food items are:
dosa, idli, fried_rice, noodles, coffee.

Rules:

- If the user asks for a price, use get_food_price.
- If the user asks for availability, use check_availability.
- If the user asks for both price AND availability,
  call BOTH tools in the SAME response.
- If the user asks something that does not require a tool,
  answer directly.
"""


# =========================================================
# AGENT SETTINGS
# =========================================================

MAX_TOKENS = 300
REPEAT_LIMIT = 3
MAX_STEPS = 6


# =========================================================
# TOOL CALL HANDLER
# =========================================================

def handle_tool_call(call, log=True):
    """
    Safely process one model-generated tool call.

    Four stages:
    1. Parse JSON
    2. Find the tool
    3. Validate arguments
    4. Execute the tool
    """

    name = call.function.name
    raw = call.function.arguments or "{}"


    # -----------------------------------------------------
    # STAGE 1: PARSE JSON
    # -----------------------------------------------------

    try:

        arguments = json.loads(raw)

    except json.JSONDecodeError as error:

        result = (
            f"Argument error: invalid JSON ({error}). "
            f"Send valid JSON for '{name}'."
        )

        if log:
            print("      ERROR: INVALID JSON")
            print("      ", result)

        return result


    # -----------------------------------------------------
    # STAGE 2: LOOK UP TOOL
    # -----------------------------------------------------

    function = TOOL_FUNCTIONS.get(name)

    if function is None:

        result = (
            f"Unknown tool: {name}. "
            f"Available tools: {', '.join(TOOL_FUNCTIONS)}."
        )

        if log:
            print("      ERROR: UNKNOWN TOOL")
            print("      ", result)

        return result


    # -----------------------------------------------------
    # STAGE 3: VALIDATE ARGUMENTS
    # -----------------------------------------------------

    problem = validate_arguments(
        arguments,
        SCHEMAS[name]
    )

    if problem:

        result = f"Argument error: {problem}"

        if log:
            print("      ERROR: VALIDATION")
            print("      ", result)

        return result


    # -----------------------------------------------------
    # STAGE 4: EXECUTE TOOL
    # -----------------------------------------------------

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
            print("      ERROR: TOOL EXECUTION")
            print("      ", result)

        return result


    if log:

        print(
            f"      {name}({arguments}) -> {result}"
        )

    return result


# =========================================================
# AGENT LOOP
# =========================================================

def agent(
    question,
    max_steps=MAX_STEPS,
    verbose=True
):

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


    # Track repeated identical tool calls
    seen = {}

    max_tokens = MAX_TOKENS


    # =====================================================
    # AGENT LOOP
    # =====================================================

    for step in range(1, max_steps + 1):


        # -------------------------------------------------
        # CALL MODEL
        # -------------------------------------------------

        response = client.chat.completions.create(

            model=MODEL,

            messages=messages,

            tools=TOOLS,

            temperature=0,

            max_tokens=max_tokens,

            # Important for the Day 6 parallel-call test
            parallel_tool_calls=True
        )


        choice = response.choices[0]
        message = choice.message


        # -------------------------------------------------
        # SHOW FINISH REASON
        # -------------------------------------------------

        if verbose:

            print(
                f"   step {step}: "
                f"finish_reason={choice.finish_reason}"
            )


        # -------------------------------------------------
        # HANDLE TRUNCATED RESPONSE
        # -------------------------------------------------

        if choice.finish_reason == "length":

            if max_tokens >= 2000:

                return (
                    "Stopped: reply remained truncated "
                    "at 2000 tokens."
                )

            max_tokens *= 2

            if verbose:

                print(
                    f"   step {step}: reply truncated."
                )

                print(
                    f"   retrying with max_tokens={max_tokens}"
                )

            continue


        # -------------------------------------------------
        # NO TOOL CALL
        # -------------------------------------------------

        if not message.tool_calls:

            return (
                message.content or ""
            ).strip()


        # -------------------------------------------------
        # SHOW TOOL CALL COUNT
        # -------------------------------------------------

        if verbose:

            print(
                f"   step {step}: "
                f"{len(message.tool_calls)} tool call(s)"
            )


        # -------------------------------------------------
        # ADD ASSISTANT TOOL CALL MESSAGE
        # -------------------------------------------------

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


        # -------------------------------------------------
        # PROCESS EVERY TOOL CALL
        # -------------------------------------------------

        for call in message.tool_calls:


            # =============================================
            # IDENTICAL CALL SIGNATURE
            # =============================================

            signature = (
                call.function.name,
                call.function.arguments
            )


            seen[signature] = (
                seen.get(signature, 0) + 1
            )


            # =============================================
            # REPEAT LIMIT
            # =============================================

            if seen[signature] >= REPEAT_LIMIT:

                return (
                    f"Stopped: {call.function.name} "
                    f"was called {REPEAT_LIMIT} times "
                    f"with the same arguments."
                )


            # =============================================
            # RUN TOOL SAFELY
            # =============================================

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


    # =====================================================
    # MAXIMUM STEPS REACHED
    # =====================================================

    return (
        "Stopped: maximum steps reached "
        "without a final answer."
    )


# =========================================================
# DAY 6 ASSESSMENT QUESTIONS
# =========================================================

if __name__ == "__main__":

    banner("DAY 6 - ROBUST CANTEEN AGENT")


    questions = [

        # -------------------------------------------------
        # QUESTION 1
        # Single tool
        # -------------------------------------------------

        "What is the price of dosa?",


        # -------------------------------------------------
        # QUESTION 2
        # Two tools / parallel tool call
        # -------------------------------------------------

        (
            "Independently check BOTH the price and availability "
            "of dosa. Use get_food_price and check_availability "
            "in the SAME response."
        ),


        # -------------------------------------------------
        # QUESTION 3
        # Invalid value
        # -------------------------------------------------

        "Try to get the price of pizza using the food price tool.",


        # -------------------------------------------------
        # QUESTION 4
        # No tool
        # -------------------------------------------------

        "Write a one-line welcome message for new students."
    ]


    # =====================================================
    # RUN ALL QUESTIONS
    # =====================================================

    for number, question in enumerate(
        questions,
        start=1
    ):

        print("\n")

        print("=" * 75)

        print(
            f"QUESTION {number}"
        )

        print("=" * 75)

        print(
            "Q:",
            question
        )

        print("=" * 75)


        try:

            answer = agent(
                question,
                verbose=True
            )


            print("\nFINAL ANSWER:")

            print(answer)


        except Exception as error:

            print("\nAGENT ERROR:")

            print(
                type(error).__name__,
                ":",
                error
            )


        print("=" * 75)