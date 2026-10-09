import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url=os.getenv("BASE_URL")
)

# Fetch and print every model ID available to you
available_models = client.models.list()

print("Available Models:")
for model in available_models:
    print(f"- {model.id}")