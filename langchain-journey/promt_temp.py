#this file contain stuffs about how prompt management can be done in langchain journey


from langchain_core.prompts import PromptTemplate
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()   

prompt = """you are a helpful assistant. 
Answer the following question: {question}."""

prompt = PromptTemplate.from_template(
    "Explain {question} in simple language."
)

formatted_prompt = prompt.invoke({
    "question": "what is rag in langchain journey"
})

print(formatted_prompt)


# model = init_chat_model(
#     model="google_genai:gemini-3.1-flash-lite",
#     temperature=0,
# )

# response = model.invoke("what is python.")
# print(response.content)