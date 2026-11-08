# this file how to we can integrate model provider in langchain journey 
#using genral method init.chat.model way

from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()   


model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)

response = model.invoke("what is python.")
print(response.content)