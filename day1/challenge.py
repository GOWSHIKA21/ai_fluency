from workflow import workflow
from agent import agent

question = "I can pay Rs. 30,000. Which two courses can I take together within this budget?"

print("=== CHALLENGE ===")
print("Q:", question)

print("\n--- WORKFLOW ---")
print(workflow(question))

print("\n--- AGENT ---")
print(agent(question))