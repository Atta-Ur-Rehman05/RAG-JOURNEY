# this is the history aware generation pipeline

from langchain_core.messages import HumanMessage, AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI

import config

llm = ChatGoogleGenerativeAI(
    model=config.LLM_MODEL,
    temperature=config.LLM_TEMPERATURE,
)

# history of the conversation
history = []

# user query
query = "What are the topics discussed in phase 1 of ai generalist?"

# add user query to history
history.append(HumanMessage(content=query))

# generate response
response = llm.invoke(history)

# add model response to history
history.append(AIMessage(content=response.content))

# print response
print(response.content)

