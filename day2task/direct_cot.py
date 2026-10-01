from config import client, MODEL, banner


QUESTIONS = [
    "What is the rental price of a projector for the college event?",
    
    "The event budget is Rs. 50,000. The venue costs Rs. 12,000, "
    "food costs Rs. 8,000, and the projector costs Rs. 5,000. "
    "How much money remains?",
    
    "The event has 120 students. Each table can seat 6 students. "
    "How many tables are needed?",
]


DIRECT_PROMPT = (
    "You are a helpful assistant. "
    "Give only the final answer. Do not explain."
)


COT_PROMPT = (
    "You are a helpful assistant. "
    "Solve the problem step by step. "
    "Number each step and show the calculation. "
    "After the steps, write the final line as: "
    "Final Answer: <answer>"
)


def ask(system_prompt, question):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": system_prompt
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    banner("DIRECT PROMPTING vs CHAIN-OF-THOUGHT")

    for number, question in enumerate(QUESTIONS, start=1):

        print("=" * 70)
        print(f"QUESTION {number}: {question}\n")

        print("--- DIRECT PROMPTING ---")
        print(ask(DIRECT_PROMPT, question))
        print()

        print("--- CHAIN-OF-THOUGHT ---")
        print(ask(COT_PROMPT, question))
        print()