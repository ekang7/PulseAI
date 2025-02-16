from pydantic import BaseModel
import json
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

def get_completion(system_prompt, user_prompt):
    chat_response = client.chat.parse(
        model=model,
        messages=[
            {
                "role": "system", 
                "content": system_prompt
            },
            {
                "role": "user", 
                "content": user_prompt
            },
        ],
        response_format=OutputFormat,
        max_tokens=1024,
        temperature=0.2
    )
    return chat_response


# response = get_completion("You are a world class researcher.", "Tell me about Michael Jordan.")

# print(response)
# print("CONTENT", response.choices[0].message.content)
# x = json.loads(response.choices[0].message.content)
# print("DICT", x)
# print("ANSWER", x['answer'])
# print("REASONING", x['reasoning_steps'])