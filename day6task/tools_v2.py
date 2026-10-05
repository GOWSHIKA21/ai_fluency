"""College Canteen tools and schemas."""

MENU = {
    "dosa": {
        "price": 40,
        "available": True
    },
    "idli": {
        "price": 30,
        "available": True
    },
    "fried_rice": {
        "price": 80,
        "available": True
    },
    "noodles": {
        "price": 70,
        "available": False
    },
    "coffee": {
        "price": 25,
        "available": True
    }
}


def get_food_price(item):
    """Return the price of a food item."""

    if item not in MENU:
        raise ValueError(f"Unknown food item: {item}")

    return f"{item} costs ₹{MENU[item]['price']}"


def check_availability(item):
    """Return whether a food item is available."""

    if item not in MENU:
        raise ValueError(f"Unknown food item: {item}")

    if MENU[item]["available"]:
        return f"{item} is available"

    return f"{item} is currently unavailable"


# ---------------------------------------------------------
# TOOL DEFINITIONS
# ---------------------------------------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "get_food_price",
            "description": "Get the price of a college canteen food item.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Food item to check.",
                        "enum": [
                            "dosa",
                            "idli",
                            "fried_rice",
                            "noodles",
                            "coffee"
                        ]
                    }
                },
                "required": ["item"],
                "additionalProperties": False
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "check_availability",
            "description": "Check whether a college canteen food item is available.",
            "parameters": {
                "type": "object",
                "properties": {
                    "item": {
                        "type": "string",
                        "description": "Food item to check.",
                        "enum": [
                            "dosa",
                            "idli",
                            "fried_rice",
                            "noodles",
                            "coffee"
                        ]
                    }
                },
                "required": ["item"],
                "additionalProperties": False
            }
        }
    }
]


# ---------------------------------------------------------
# FUNCTIONS
# ---------------------------------------------------------

TOOL_FUNCTIONS = {
    "get_food_price": get_food_price,
    "check_availability": check_availability
}


# ---------------------------------------------------------
# SINGLE SOURCE OF TRUTH FOR VALIDATION
# ---------------------------------------------------------

SCHEMAS = {
    "get_food_price": TOOLS[0]["function"]["parameters"],
    "check_availability": TOOLS[1]["function"]["parameters"]
}