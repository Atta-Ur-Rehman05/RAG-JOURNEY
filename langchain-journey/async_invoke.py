import asyncio
from langchain.chat_models import init_chat_model
import os
from dotenv import load_dotenv
load_dotenv()   


model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)

async def main():

    questions = [
        "Define RAG.",
        "Explain advantages of RAG.",
        "Explain disadvantages of RAG."
    ]

    responses = await asyncio.gather(
        *[
            model.ainvoke(question)
            for question in questions
        ]
    )

    for response in responses:
        print(response.content)
        print("----------------")

asyncio.run(main())