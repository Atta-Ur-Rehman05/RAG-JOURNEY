# this file contain streaming logic for the language model
#what is streaming : Streaming is a technique where the output of a model is generated and returned in real-time, as opposed to waiting for the entire output to be generated before returning it.


from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

import os
from dotenv import load_dotenv
load_dotenv()   

prompt = """you are a helpful assistant.
Answer the following question: {question}."""

prompt = PromptTemplate.from_template(
    "Explain {question} in simple language."
)

model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
    streaming = True
)

chain = prompt | model | StrOutputParser()

for chunk in chain.stream({"question": "RAG?"}   ):
    print(chunk, end="", flush=True)


# response = model.invoke("what is python.")
# print(response.content)