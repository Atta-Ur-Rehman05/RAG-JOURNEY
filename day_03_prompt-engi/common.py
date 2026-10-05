import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()  # reads GEMINI_API_KEY from a .env file if present

MODEL = "gemini-3.5-flash"
client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


# --- 🎨 TEXT FORMATTING ---
# Enable ANSI escape sequences in Windows terminal
os.system("")

# ANSI Color Codes
CYAN = "\033[96m"
GREEN = "\033[92m"
YELLOW = "\033[93m"
DIM = "\033[90m"
BOLD = "\033[1m"
RESET = "\033[0m"


# --- 🛠️ CORE AI FUNCTIONS ---

system_prompt=input(f"{BOLD}{CYAN}👤 System Prompt ❯ {RESET}").strip()
user_text=input(f"{BOLD}{CYAN}👤 User Text ❯ {RESET}").strip()

def ask(system_prompt: str, user_text: str, **params) -> str:
    """Send one system prompt plus one user message and return the reply text."""

    
    response = client.chat.completions.create(
        model=MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_text},
        ],
        **params,
    )
    print(response.choices[0].message.content)

ask(system_prompt,user_text)