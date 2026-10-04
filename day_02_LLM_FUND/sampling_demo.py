from openai import OpenAI
import os 
from dotenv import load_dotenv

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

prompt = "Write one short sentence about the sky."

for temperature in (0.0, 1.0, 2.0):
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=[{"role": "user", "content": prompt}],
        temperature=temperature,
    )
    print(f"temperature={temperature}:")
    print(response.choices[0].message.content)
    print("-" * 40)