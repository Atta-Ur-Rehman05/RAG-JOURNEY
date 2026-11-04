"""
Day 05: Tool Calling (Function Calling) with Gemini / OpenAI API
===============================================================

What is Tool Calling?
---------------------
Tool Calling (Function Calling) empowers an LLM to recognize when it needs
external capabilities (such as real-time weather, database lookups, or calculations)
and return a structured request (tool name + JSON arguments) rather than guessing
or hallucinating.

The Tool Calling Lifecycle:
1. Define the Python tool (e.g. `get_current_weather`).
2. Describe the tool to the LLM via JSON Schema (`tools` parameter).
3. Send user query + tool definitions to the LLM.
4. If relevant, the LLM returns `tool_calls` with function name and arguments.
5. Your application runs the local Python function with those arguments.
6. Return the tool output to the LLM with `role: "tool"` and matching `tool_call_id`.
7. The LLM generates the final conversational response based on the actual tool result.
"""

import json
import os
import random
from dotenv import load_dotenv
from openai import OpenAI

# Load API keys from .env
load_dotenv()

# Initialize OpenAI client pointing to Gemini endpoint
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.1-flash-lite")


# =====================================================================
# 1. TOOL IMPLEMENTATION (Local Python function)
# =====================================================================

MOCK_WEATHER_DB = {
    "tokyo": {"temp_c": 18, "condition": "Sunny ☀️", "humidity": "45%", "wind": "12 km/h"},
    "london": {"temp_c": 12, "condition": "Light Rain 🌧️", "humidity": "82%", "wind": "20 km/h"},
    "new york": {"temp_c": 22, "condition": "Partly Cloudy ⛅", "humidity": "55%", "wind": "15 km/h"},
    "paris": {"temp_c": 16, "condition": "Overcast ☁️", "humidity": "68%", "wind": "10 km/h"},
    "karachi": {"temp_c": 32, "condition": "Clear and Warm ☀️", "humidity": "60%", "wind": "18 km/h"},
    "lahore": {"temp_c": 29, "condition": "Hazy Sunshine 🌤️", "humidity": "50%", "wind": "8 km/h"},
    "islamabad": {"temp_c": 24, "condition": "Pleasant 🌤️", "humidity": "46%", "wind": "11 km/h"},
    "sydney": {"temp_c": 21, "condition": "Breezy 🍃", "humidity": "58%", "wind": "25 km/h"},
}


def get_current_weather(location: str, unit: str = "celsius") -> dict:
    """
    Fetch current weather details for a given city/location.

    Args:
        location (str): Name of the city (e.g. "Tokyo", "London").
        unit (str): "celsius" or "fahrenheit". Default is "celsius".

    Returns:
        dict: Weather report with temperature, condition, humidity, and wind speed.
    """
    city_key = location.lower().strip()

    # Look up in database or generate realistic values for any city
    if city_key in MOCK_WEATHER_DB:
        data = MOCK_WEATHER_DB[city_key].copy()
    else:
        data = {
            "temp_c": random.randint(15, 30),
            "condition": random.choice(["Sunny ☀️", "Partly Cloudy ⛅", "Clear Sky 🌤️", "Light Showers 🌦️"]),
            "humidity": f"{random.randint(40, 75)}%",
            "wind": f"{random.randint(8, 22)} km/h",
        }

    temp = data["temp_c"]
    if unit.lower() == "fahrenheit":
        temp = round((temp * 9 / 5) + 32, 1)
        temp_str = f"{temp}°F"
    else:
        temp_str = f"{temp}°C"

    return {
        "location": location.title(),
        "temperature": temp_str,
        "condition": data["condition"],
        "humidity": data["humidity"],
        "wind_speed": data["wind"],
    }


# =====================================================================
# 2. TOOL SCHEMA DEFINITIONS (OpenAI JSON Schema specification)
# =====================================================================

tools = [
    {
        "type": "function",
        "function": {
            "name": "get_current_weather",
            "description": "Get current weather condition, temperature, humidity, and wind speed for a specified location.",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state/country, e.g. London, Tokyo, Karachi, New York.",
                    },
                    "unit": {
                        "type": "string",
                        "enum": ["celsius", "fahrenheit"],
                        "description": "Temperature unit: 'celsius' or 'fahrenheit'. Default is celsius.",
                    },
                },
                "required": ["location"],
            },
        },
    }
]

# Dispatcher mapping function names to callable functions
AVAILABLE_TOOLS = {
    "get_current_weather": get_current_weather,
}


def execute_tool_call(tool_name: str, arguments: dict) -> dict:
    """Executes the matching Python function for a requested tool call."""
    tool_func = AVAILABLE_TOOLS.get(tool_name)
    if tool_func:
        return tool_func(**arguments)
    return {"error": f"Tool '{tool_name}' is not recognized."}


# =====================================================================
# 3. TOOL CALLING PIPELINE
# =====================================================================

def ask_with_weather_tool(user_query: str) -> str:
    """
    Executes the full tool calling workflow for a single query:
      1. Calls LLM with tool definitions.
      2. If tool call is returned, runs the Python function.
      3. Sends tool results back to LLM for final generation.
    """
    messages = [
        {
            "role": "system",
            "content": "You are a helpful assistant. Use the provided tools when asked for weather data.",
        },
        {"role": "user", "content": user_query},
    ]

    print(f"\n[1] User Query: \"{user_query}\"")

    # Step 1: LLM determines whether tool calling is required
    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        tools=tools,
        tool_choice="auto",
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    if tool_calls:
        print(f"[2] LLM triggered {len(tool_calls)} tool call(s):")
        messages.append(response_message)

        # Step 2: Execute each tool call requested
        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            tool_call_id = tool_call.id

            print(f"    🛠️ Executing: {function_name}({function_args})")
            result = execute_tool_call(function_name, function_args)
            print(f"    📦 Result: {result}")

            # Step 3: Append the tool execution result
            messages.append({
                "role": "tool",
                "tool_call_id": tool_call_id,
                "name": function_name,
                "content": json.dumps(result),
            })

        # Step 4: Final response from LLM using tool data
        print("[3] Sending tool result back to LLM for final answer...")
        final_response = client.chat.completions.create(
            model=MODEL,
            messages=messages,
        )
        return final_response.choices[0].message.content
    else:
        print("[2] No tool call needed. Direct response generated.")
        return response_message.content


# =====================================================================
# 4. RUN DEMO
# =====================================================================

if __name__ == "__main__":
    queries = [
        "What's the weather like in Tokyo right now?",
        "Can you compare the current weather between Karachi and London in Fahrenheit?",
        "What is the capital of France?",  # Doesn't need weather tool
    ]

    for q in queries:
        print("\n" + "=" * 65)
        reply = ask_with_weather_tool(q)
        print(f"\n🤖 Final Answer:\n{reply}")
