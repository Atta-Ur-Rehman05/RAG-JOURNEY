#this file contain the chaining logic for the language model

from langchain.chat_models import init_chat_model
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from dotenv import load_dotenv

load_dotenv()

template = """You are a helpful assistant.
Answer the following question: {question}."""

template = PromptTemplate.from_template(template)

 
model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)

output_parser = StrOutputParser()

chain = template | model | output_parser

response = chain.invoke({ "question": "What is LangChain?" })

print(response)
