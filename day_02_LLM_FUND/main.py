import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Enable ANSI escape sequences in Windows terminal
os.system("")

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"

conversation = []

print(f"{CYAN}╭───────────────────────────────────────────────────╮{RESET}")
print(f"{CYAN}│{RESET}  {BOLD}✨ Gemini CLI Chatbot{RESET}                           {CYAN}│{RESET}")
print(f"{CYAN}│{RESET}  {DIM}Type 'quit' or 'exit' to end the session{RESET}         {CYAN}│{RESET}")
print(f"{CYAN}╰───────────────────────────────────────────────────╯{RESET}\n")

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

    print(f"\n{BOLD}{GREEN}🤖 Gemini ❯ {RESET}", end="", flush=True)

    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=conversation,
        stream=True,
        temperature=0.5
        
    )

    response_text = ""
    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            print(content, end="", flush=True)
            response_text += content
    print(f"\n\n{DIM}{'─' * 55}{RESET}\n")

    conversation.append({"role": "assistant", "content": response_text})




