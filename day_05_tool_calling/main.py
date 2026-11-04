import json
import os
from dotenv import load_dotenv
from openai import OpenAI
from tool_calling import execute_tool_call, tools

# Load environment variables
load_dotenv()

# Initialize OpenAI client with Gemini compatibility endpoint
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

MODEL = os.getenv("GEMINI_MODEL", "gemini-3.5-flash-lite")

# Enable ANSI escape sequences in Windows terminal
os.system("")

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
MAGENTA = "\033[95m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


def print_banner():
    print(f"{CYAN}╭───────────────────────────────────────────────────╮{RESET}")
    print(f"{CYAN}│{RESET}  {BOLD}🌦️  Gemini Weather Chatbot (Tool Calling){RESET}       {CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {DIM}Ask about weather in any city (e.g., Tokyo, London){RESET}{CYAN}│{RESET}")
    print(f"{CYAN}│{RESET}  {DIM}Type 'quit' or 'exit' to end the session{RESET}         {CYAN}│{RESET}")
    print(f"{CYAN}╰───────────────────────────────────────────────────╯{RESET}\n")


def chat_loop():
    print_banner()

    conversation = [
        {
            "role": "system",
            "content": (
                "You are a friendly, helpful assistant. You have access to weather tools. "
                "Whenever a user asks for weather or temperature conditions, call the appropriate tool. "
                "Format temperature and conditions clearly in your responses."
            ),
        }
    ]

    while True:
        try:
            user_input = input(f"{BOLD}{CYAN}👤 You ❯ {RESET}").strip()
        except (KeyboardInterrupt, EOFError):
            print(f"\n{YELLOW}Session ended. Goodbye! 👋{RESET}")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit"):
            print(f"\n{YELLOW}Goodbye! 👋{RESET}")
            break

        conversation.append({"role": "user", "content": user_input})

        # Step 1: Initial call with tools provided
        response = client.chat.completions.create(
            model=MODEL,
            messages=conversation,
            tools=tools,
            tool_choice="auto",
        )

        response_message = response.choices[0].message
        tool_calls = response_message.tool_calls

        # Step 2: Handle tool calls if requested by the model
        if tool_calls:
            # Append model's tool call request to the conversation history
            conversation.append(response_message)

            for tool_call in tool_calls:
                fn_name = tool_call.function.name
                fn_args = json.loads(tool_call.function.arguments)

                print(f"\n{MAGENTA}  [🛠️  Tool Call]{RESET} {BOLD}{fn_name}{RESET}({fn_args})")
                tool_output = execute_tool_call(fn_name, fn_args)
                print(f"{DIM}  [📦 Tool Result]{RESET} {tool_output}")

                # Send tool execution result back to conversation
                conversation.append({
                    "role": "tool",
                    "tool_call_id": tool_call.id,
                    "name": fn_name,
                    "content": json.dumps(tool_output),
                })

            # Step 3: Get final answer with tool outputs included
            final_response = client.chat.completions.create(
                model=MODEL,
                messages=conversation,
            )
            final_content = final_response.choices[0].message.content or ""
            print(f"\n{BOLD}{GREEN}🤖 Gemini ❯ {RESET}{final_content}")
            conversation.append({"role": "assistant", "content": final_content})
        else:
            # Direct response when no tool is required
            reply = response_message.content or ""
            print(f"\n{BOLD}{GREEN}🤖 Gemini ❯ {RESET}{reply}")
            conversation.append({"role": "assistant", "content": reply})

        print(f"\n{DIM}{'─' * 55}{RESET}\n")


if __name__ == "__main__":
    chat_loop()
