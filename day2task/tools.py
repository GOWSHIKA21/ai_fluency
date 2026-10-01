# Tool functions for the college event scenario

EQUIPMENT_PRICES = {
    "projector": 5000,
    "microphone": 2500,
    "speaker": 4000
}


def get_equipment_price(item):
    """Return the rental price of an event equipment item."""
    item = item.lower()

    if item in EQUIPMENT_PRICES:
        return EQUIPMENT_PRICES[item]

    return None


def calculator(expression):
    """Calculate a mathematical expression."""
    return eval(expression, {"__builtins__": {}}, {})