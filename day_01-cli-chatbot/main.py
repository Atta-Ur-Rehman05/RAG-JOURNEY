import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

conversation = []
print("Chatbot started. Type 'quit' to exit.")

# enable the streaming

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    conversation.append({"role": "user", "content": user_input})
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=conversation,
        stream=True,
    )
    # for chunk in response:
    #     print(chunk.choices[0].delta.content)
    
    response_text = ""  
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            response_text += content
    print()
    
    conversation.append({"role": "assistant", "content": response_text})




