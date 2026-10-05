"""Day 6: Fault injection without using the model."""

import json

from robust_agent import handle_tool_call


class FakeFunction:

    def __init__(self, name, arguments):

        self.name = name
        self.arguments = arguments


class FakeCall:

    def __init__(
        self,
        name,
        arguments,
        call_id="test_call"
    ):

        self.id = call_id
        self.type = "function"

        self.function = FakeFunction(
            name,
            arguments
        )


FAULTS = [

    # -----------------------------------------------------
    # GOOD CALL
    # -----------------------------------------------------

    (
        "Good call",
        FakeCall(
            "get_food_price",
            '{"item": "dosa"}'
        )
    ),


    # -----------------------------------------------------
    # 1. INVALID JSON
    # -----------------------------------------------------

    (
        "Invalid JSON",
        FakeCall(
            "get_food_price",
            '{"item": "dosa"'
        )
    ),


    # -----------------------------------------------------
    # 2. UNKNOWN TOOL
    # -----------------------------------------------------

    (
        "Unknown tool",
        FakeCall(
            "get_food_rating",
            '{"item": "dosa"}'
        )
    ),


    # -----------------------------------------------------
    # 3. MISSING REQUIRED
    # -----------------------------------------------------

    (
        "Missing required",
        FakeCall(
            "get_food_price",
            '{}'
        )
    ),


    # -----------------------------------------------------
    # 4. WRONG TYPE
    # -----------------------------------------------------

    (
        "Wrong type",
        FakeCall(
            "get_food_price",
            '{"item": 123}'
        )
    ),


    # -----------------------------------------------------
    # 5. VALUE OUTSIDE ENUM
    # -----------------------------------------------------

    (
        "Invalid enum value",
        FakeCall(
            "get_food_price",
            '{"item": "pizza"}'
        )
    ),


    # -----------------------------------------------------
    # 6. INVENTED ARGUMENT
    # -----------------------------------------------------

    (
        "Invented argument",
        FakeCall(
            "get_food_price",
            '{"item": "dosa", "discount": 50}'
        )
    ),


    # -----------------------------------------------------
    # 7. WRONG CASE
    # -----------------------------------------------------

    (
        "Wrong case value",
        FakeCall(
            "get_food_price",
            '{"item": "Dosa"}'
        )
    ),


    # -----------------------------------------------------
    # 8. EMPTY ARGUMENT STRING
    # -----------------------------------------------------

    (
        "Empty arguments",
        FakeCall(
            "get_food_price",
            ""
        )
    ),

]


if __name__ == "__main__":

    print("=" * 80)

    print("DAY 6 - FAULT INJECTION")

    print("=" * 80)


    for label, call in FAULTS:

        result = handle_tool_call(
            call,
            log=False
        )

        print(
            f"\n{label:<25} -> {result}"
        )


    print("\n" + "=" * 80)

    print(
        "All faults returned strings without crashing."
    )

    print("=" * 80)