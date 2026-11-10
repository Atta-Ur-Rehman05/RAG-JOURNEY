from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)



for response in model.batch_as_completed([
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
]):
    print(response)