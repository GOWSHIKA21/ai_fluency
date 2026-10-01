from config import client, MODEL

question = "What is the fee for CS101?"

response = client.chat.completions.create(
    model=MODEL,
    messages=[
        {"role": "user", "content": question}
    ]
)

print("QUESTION:", question)
print("\nANSWER:", response.choices[0].message.content)