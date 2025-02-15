import requests
import simplejson as json
from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


class AnswerFormat(BaseModel):
    answer: str
    reasoning: str


url = "https://api.perplexity.ai/chat/completions"
headers = {"Authorization": "Bearer " + PERPLEXITY_API_KEY}

def get_completion(system_prompt, user_prompt):
    payload = {
        "model": "sonar-pro",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt +" Please output a JSON object containing the following fields: " + "answer, reasoning"},
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": AnswerFormat.model_json_schema()},
        },
    }
    response = requests.post(url, headers=headers, json=payload).json()
    raw_content = response["choices"][0]["message"]["content"].strip()
    if not raw_content:
        print("Warning: The API response is empty. Full response:")
        print(response)
        return {"answer": "No answer returned", "reasoning": ""}
    try:
        content = json.loads(raw_content, strict=False)
    except Exception as e:
        print("Error decoding JSON. Raw content:")
        print(raw_content)
        print("Full response:")
        print(response)
        raise e
    return content

print(get_completion(
    "You are a world class researcher.",
    "Tell me about Michael Jordan."
)['answer'])