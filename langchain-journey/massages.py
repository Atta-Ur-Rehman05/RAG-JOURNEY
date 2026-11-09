# this file contain the detail about how massages can be done in langchain journey

#following are the types of massages that can be done in langchain journey
#1 system massage : This is a message that is sent to the language model to set the context or provide instructions for the conversation.
#2 ai massage : This is a message that is sent by the language model to the user.
#3human massage : This is a message that is sent by a human to the language model.

from langchain.chat_models import init_chat_model
from langchain_core.messages import (SystemMessage, AIMessage, HumanMessage)
import os
from dotenv import load_dotenv

load_dotenv()

model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)

messages = [
    SystemMessage(content="You are a helpful assistant."),
    HumanMessage(content="What is the capital of France?")
]

response = model.invoke(messages)
print(response)
