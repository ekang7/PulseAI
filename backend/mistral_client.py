from pydantic import BaseModel

class Book(BaseModel):
    name: str
    authors: list[str]
    
import os
from mistralai import Mistral

api_key = os.environ["MISTRAL_API_KEY"]
model = "ministral-8b-latest"

client = Mistral(api_key=api_key)

chat_response = client.chat.parse(
    model=model,
    messages=[
        {
            "role": "system", 
            "content": "Extract the books information."
        },
        {
            "role": "user", 
            "content": "I recently read 'To Kill a Mockingbird' by Harper Lee."
        },
    ],
    response_format=Book,
    max_tokens=256,
    temperature=0
)