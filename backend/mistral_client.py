from pydantic import BaseModel
import os
from mistralai import Mistral
from dotenv import load_dotenv
load_dotenv() 
MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")

class OutputFormat(BaseModel):
    answer: str
    reasoning_steps: str
    
model = "pixtral-large-latest"

client = Mistral(api_key=MISTRAL_API_KEY)

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
    response_format=OutputFormat,
    max_tokens=256,
    temperature=0
)

print(chat_response)