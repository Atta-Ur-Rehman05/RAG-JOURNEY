import os

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from streamlit.runtime.scriptrunner import get_script_run_ctx

load_dotenv()

client = OpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)


def stream_chat_response(messages):
    response = client.chat.completions.create(
        model="gemini-3.1-flash-lite",
        messages=messages,
        stream=True,
    )

    for chunk in response:
        content = chunk.choices[0].delta.content
        if content:
            yield content


def run_cli_chat():
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

        response_text = ""
        for content in stream_chat_response(conversation):
            print(content, end="", flush=True)
            response_text += content

        print(f"\n\n{DIM}{'─' * 55}{RESET}\n")
        conversation.append({"role": "assistant", "content": response_text})


def run_streamlit_chat():
    st.set_page_config(page_title="Gemini Chatbot", page_icon="🤖")

    if "conversation" not in st.session_state:
        st.session_state.conversation = []

    st.title("✨ Gemini Chatbot")
    st.caption("Chat with Gemini in a simple Streamlit interface.")

    if st.button("Clear chat"):
        st.session_state.conversation = []

    for message in st.session_state.conversation:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    user_input = st.chat_input("Type your message here...")

    if user_input:
        st.session_state.conversation.append({"role": "user", "content": user_input})

        with st.chat_message("user"):
            st.markdown(user_input)

        with st.chat_message("assistant"):
            response_placeholder = st.empty()
            response_text = ""
            stream = stream_chat_response(st.session_state.conversation)

            for content in stream:
                response_text += content
                response_placeholder.markdown(response_text + "▌")

            response_placeholder.markdown(response_text)

        st.session_state.conversation.append({"role": "assistant", "content": response_text})


def main():
    if get_script_run_ctx(suppress_warning=True) is not None:
        run_streamlit_chat()
    else:
        run_cli_chat()


if __name__ == "__main__":
    main()

