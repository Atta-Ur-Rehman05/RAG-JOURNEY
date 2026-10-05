from openai import OpenAI
import os 
from dotenv import load_dotenv 

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


SYSTEM_PROMPT = """ You are an email summarizer. Read the email the user pastes and produce exactly these lines: 
TL;DR: one sentence. 
Key points: up to 3 short bullets. 
Action needed: what the reader must do, or "None". 
Deadline: the date or timeframe, or "None mentioned". 
Rules:
- Use only information in the email. Do not add opinions.
- If the email is under 30 words, return only the TL;DR line.
- No introduction or closing remarks. """ 

emails = """
hey atta you are informed that you have been selected for the jnr voice captan role in aws must club 
, your requested to send your docs and ensure your presence in coming tuesday meeting,
and we are happy to inform you that you are eligible to attend the leadership training in bangkok next month,
please ensure your presence and send you documents as soon as possible to the HR department.
"""

    
    
response = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": emails},
    ],
)

print(response.choices[0].message.content)