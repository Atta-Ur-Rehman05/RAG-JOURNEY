#this file contain how we can call tools using langchain


from langchain.chat_models import init_chat_model
from langchain.tools import tool
import os
from dotenv import load_dotenv
load_dotenv()   


model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)




@tool                                  
def get_weather(location: str) -> str:
    """Get the weather at a location."""
    return f"It's sunny in {location}."

model_with_tools = model.bind_tools([get_weather])

response =model_with_tools.invoke("What's the weather like in Boston?")
for tool_call in response.tool_calls:
    # View tool calls made by the model
    print(f"Tool: {tool_call['name']}")
    print(f"Args: {tool_call['args']}")


    