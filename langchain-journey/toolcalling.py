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

# model_with_tools = model.bind_tools([get_weather])

# response =model_with_tools.invoke("What's the weather like in Boston?")
# for tool_call in response.tool_calls:
#     # View tool calls made by the model
#     print(f"Tool: {tool_call['name']}")
#     print(f"Args: {tool_call['args']}")


    
#     # Bind (potentially multiple) tools to the model
# tools = [get_weather]
# tools_by_name = {tool.name: tool for tool in tools}
# model_with_tools = model.bind_tools(tools)

# # Step 1: Model generates tool calls
# messages = [{"role": "user", "content": "What's the weather in Boston?"}]
# ai_msg = model_with_tools.invoke(messages)
# messages.append(ai_msg)

# # Step 2: Execute tools and collect results
# for tool_call in ai_msg.tool_calls:
#     # Execute the tool with the generated arguments
#     tool = tools_by_name[tool_call["name"]]
#     tool_result = tool.invoke(tool_call)
#     messages.append(tool_result)

# # Step 3: Pass results back to model for final response
# final_response = model_with_tools.invoke(messages)
# print(final_response.text)
# # "The current weather in Boston is 72°F and sunny."



# parralllel tool calling 

tools = [get_weather]
tools_by_name = {tool.name: tool for tool in tools}
model_with_tools = model.bind_tools(tools)

response = model_with_tools.invoke(
    "What's the weather in Boston and Tokyo?"
)


# The model may generate multiple tool calls
print(response.tool_calls)
# [
#   {'name': 'get_weather', 'args': {'location': 'Boston'}, 'id': 'call_1'},
#   {'name': 'get_weather', 'args': {'location': 'Tokyo'}, 'id': 'call_2'},
# ]


# Execute all tools (can be done in parallel with async)
results = []
for tool_call in response.tool_calls:
    tool = tools_by_name[tool_call["name"]]
    result = tool.invoke(tool_call)
    results.append(result)