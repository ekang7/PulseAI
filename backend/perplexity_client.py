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


payload = {
    "model": "sonar-pro",
    "messages": [
        {"role": "system", "content": "Be precise and concise."},
        {"role": "user", "content": (
            "Tell me about Michael Jordan. "
            "Please output a JSON object containing the following fields: "
            "answer, reasoning"
        )},
    ],
    "response_format": {
        "type": "json_schema",
        "json_schema": {"schema": AnswerFormat.model_json_schema()},
    },
}
response = requests.post(url, headers=headers, json=payload).json()
print(response)
raw_content = response["choices"][0]["message"]["content"].strip()
content = json.loads(raw_content, strict=False)
print("Full response:")
print(content)
print("\nJust the answer:")
print(content["answer"])
