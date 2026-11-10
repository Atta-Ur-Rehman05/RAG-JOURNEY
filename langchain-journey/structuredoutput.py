#this file contain the structured output using pydantic model

# this file how to we can integrate model provider in langchain journey 
#using genral method init.chat.model way

from langchain.chat_models import init_chat_model
from pydantic import BaseModel , Field
import os
from dotenv import load_dotenv
load_dotenv()   

class movie(BaseModel):
    """A Pydantic model representing a movie. with details:"""

    title: str = Field(..., description="The title of the movie")
    year: int = Field(..., description="The release year of the movie")
    director: str = Field(..., description="The director of the movie")
    genre: str = Field(..., description="The genre of the movie")


model = init_chat_model(
    model="google_genai:gemini-3.1-flash-lite",
    temperature=0,
    
)

model_with_structured_output = model.with_structured_output(movie, include_raw=True)

response = model_with_structured_output.invoke("Provide details about the movie Inception.")
print(response)