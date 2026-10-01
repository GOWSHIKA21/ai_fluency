from config import client, MODEL

def ask_chatbot(question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a helpful college event assistant."
            },
            {
                "role": "user",
                "content": question
            }
        ]
    )

    return response.choices[0].message.content


questions = [
    "What is the registration fee for TECHFEST2026?",
    "What is the total cost of TECHFEST2026 and AIWORKSHOP2026 after a 10% discount?",
    "Is TECHFEST2026 more expensive than AIWORKSHOP2026? If yes, by how much?",
    "Give me a two-line welcome message for the college events."
]

for question in questions:
    print("\nQuestion:", question)
    print("Answer:", ask_chatbot(question))