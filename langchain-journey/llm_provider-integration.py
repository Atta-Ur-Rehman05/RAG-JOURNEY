# this file contains the integration of LLM providers with LangChain, 
# allowing users to easily switch between different LLMs for their applications.


import os
from langchain.chat_models import init_chat_model
from langchain_google_genai import ChatGoogleGenerativeAI

  

# model =ChatOpenAI(
#     model_name="gpt-4",
#     temperature=0
# )

model = ChatGoogleGenerativeAI(

    model_name="google_genai:gemini-3.7-flash",
  
    temperature=0



)

response = model.invoke("Hello, how are you?")

print(response.content)

