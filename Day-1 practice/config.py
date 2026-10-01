import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

PROVIDER = os.getenv("PROVIDER")
MODEL = os.getenv("MODEL")

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

EVENTS = {
    "TECHFEST2026": {
        "fee": 500,
        "capacity": 100
    },
    "HACKATHON2026": {
        "fee": 300,
        "capacity": 50
    },
    "AIWORKSHOP2026": {
        "fee": 200,
        "capacity": 30
    }
}

QUESTIONS = [
    "What is the registration fee for TECHFEST2026?",
    "What is the total cost of TECHFEST2026 and AIWORKSHOP2026 after a 10% discount?",
    "Is TECHFEST2026 more expensive than AIWORKSHOP2026? If yes, by how much?",
    "Give me a two-line welcome message for the college events."
]