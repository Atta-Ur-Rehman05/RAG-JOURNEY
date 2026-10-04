import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

response = client.chat.completions.create(
    model="gemini-3.1-flash-lite",
    messages=[{"role": "user", "content": "Write one short sentence about the sky."}],
    max_tokens=1024,
)

usage = response.usage 
print("Reply:        ", response.choices[0].message.content) 
print("Finish reason:", response.choices[0].finish_reason)   # "length" = cut off 
print("Input tokens: ", usage.prompt_tokens) 
print("Output tokens:", usage.completion_tokens) 
print("Total tokens: ", usage.total_tokens)

# Thinking tokens, when the endpoint reports them separately
details = getattr(usage, "completion_tokens_details", None) 
if details is not None and getattr(details, "reasoning_tokens", None) is not None:    
    print("Thinking tokens:", details.reasoning_tokens)