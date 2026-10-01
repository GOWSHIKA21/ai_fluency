from config import EVENTS


def get_fee(event_name):
    event = EVENTS.get(event_name)

    if event:
        return event["fee"]

    return None


def process_question(question):
    question_lower = question.lower()

    # Question 1
    if "fee" in question_lower and "techfest2026" in question_lower:
        fee = get_fee("TECHFEST2026")
        return f"The registration fee for TECHFEST2026 is ₹{fee}."

    # Question 2
    elif "total" in question_lower and "discount" in question_lower:
        fee1 = get_fee("TECHFEST2026")
        fee2 = get_fee("AIWORKSHOP2026")

        total = fee1 + fee2
        discount = total * 0.10
        final_amount = total - discount

        return f"The total cost after a 10% discount is ₹{final_amount:.0f}."

    # Question 3
    elif "more expensive" in question_lower:
        fee1 = get_fee("TECHFEST2026")
        fee2 = get_fee("AIWORKSHOP2026")

        difference = fee1 - fee2

        if difference > 0:
            return f"Yes. TECHFEST2026 is more expensive by ₹{difference}."
        else:
            return "No. TECHFEST2026 is not more expensive."

    # Question 4
    elif "welcome" in question_lower:
        return "Welcome to our college events!\nEnjoy learning, innovation, and fun together."

    else:
        return "Sorry, I cannot handle this question."


questions = [
    "What is the registration fee for TECHFEST2026?",
    "What is the total cost of TECHFEST2026 and AIWORKSHOP2026 after a 10% discount?",
    "Is TECHFEST2026 more expensive than AIWORKSHOP2026? If yes, by how much?",
    "Give me a two-line welcome message for the college events."
]


for question in questions:
    print("\nQuestion:", question)
    print("Answer:", process_question(question))