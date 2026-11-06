# this file contains the integration of LLM providers with LangChain, 
# allowing users to easily switch between different LLMs for their applications.

from langchain import openai

model = openai.OpenAI(
    model_name="text-davinci-003",
    temperature=0
)

response = model.generate("Hello, how are you?")

print(response.content)

