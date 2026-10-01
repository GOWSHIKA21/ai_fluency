FEES = {
    "CS101": 12000,
    "AI202": 18000,
    "DS303": 15000
}


def get_course_fee(course_code):
    return FEES.get(course_code)


def calculator(expression):
    return eval(expression, {"__builtins__": {}}, {})