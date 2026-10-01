from collections import Counter
from config import client, MODEL, banner


QUESTION = (
    "The event has 120 students. Each table can seat 6 students. "
    "How many tables are needed?"
)


def ask(question, temperature):
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {
                "role": "system",
                "content": (
                    "Solve the problem step by step. "
                    "Show the calculation and give the final answer clearly."
                )
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=temperature
    )

    return response.choices[0].message.content.strip()


if __name__ == "__main__":

    banner("SELF-CONSISTENCY")

    print("QUESTION:")
    print(QUESTION)
    print()

    answers = []

    for i in range(5):
        answer = ask(QUESTION, 0.8)
        answers.append(answer)

        print(f"--- RUN {i + 1} ---")
        print(answer)
        print()

    print("=" * 70)
    print("SELF-CONSISTENCY OBSERVATION")
    print("=" * 70)

    print("Five responses were generated with temperature = 0.8.")
    print("The answers may use different wording or reasoning paths.")
    print("Check whether the final numerical answer is consistent.")

    print()
    print("Now comparing with temperature = 0:")

    deterministic_answers = []

    for i in range(5):
        answer = ask(QUESTION, 0)
        deterministic_answers.append(answer)

        print(f"--- TEMP 0 RUN {i + 1} ---")
        print(answer)
        print()

    print("=" * 70)
    print("CONCLUSION")
    print("=" * 70)
    print(
        "Higher temperature can produce more variation in responses, "
        "while temperature 0 generally produces more consistent responses."
    )