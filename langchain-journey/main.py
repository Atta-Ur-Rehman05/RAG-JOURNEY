# integrating google model

from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()


model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)

response = model.invoke("Write a poem about the beauty of nature.")

print(response.content)

