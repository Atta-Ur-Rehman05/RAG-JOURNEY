import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/models/",
)

response = client.chat.completions.create(
    model="gemma-3-27b-it",
    messages=[
        {"role": "user", "content": "write a one sentence story about fastapi"}
    ],
)

print(response.choices[0].message.content)
