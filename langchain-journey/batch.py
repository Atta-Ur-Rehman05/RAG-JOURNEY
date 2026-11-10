from langchain.chat_models import init_chat_model
from dotenv import load_dotenv
import os
load_dotenv()

model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
)



responses = model.batch([                              # what does batch do is : Batching a collection of independent requests to a model can significantly improve performance and reduce costs, as the processing can be done in parallel
    "Why do parrots have colorful feathers?",
    "How do airplanes fly?",
    "What is quantum computing?"
])
for response in responses:
    print(response)