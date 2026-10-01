from config import client, MODEL
from fee_tool import read_fees

question = "What is the fee for CS101?"

fees = read_fees()

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {
            "role": "system",
            "content": "Answer the user's question using the fee information provided by the tool."
        },
        {
            "role": "user",
            "content": question
        },
        {
            "role": "system",
            "content": f"Tool result from read_fees():\n{fees}"
        }
    ]
)

print("QUESTION:", question)
print("\nTOOL CALLED: read_fees()")
print("\nTOOL RESULT:")
print(fees)
print("\nFINAL ANSWER:", response.choices[0].message.content)