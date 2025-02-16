import requests
import simplejson as json
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from typing import List

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {"Authorization": "Bearer " + PERPLEXITY_API_KEY}
MODEL = "sonar"

class Response(BaseModel):
    thoughts: str
    answer: str

def get_search_response(user_prompt : str) -> Response:    
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Please provide a precise answer. Output a JSON object with fields `thoughts` and `answer`. Your `thoughts` should be a deliberation of details that the user may want to know. Then, provide your `answer`."
            },
            {
                "role": "user",
                "content": user_prompt
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": Response.model_json_schema()},
        },
    }
    response = requests.post(URL, headers=HEADERS, json=payload).json()
    raw_content = ...
    try:
        raw_content = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        print("Warning: The API response is empty. Full response:")
        print(response)
        raise e

    try:
        content = json.loads(raw_content, strict=False)
        return Response(**content)
    except Exception as e:
        print("Error decoding JSON. Raw content:")
        print(raw_content)
        print("Full response:")
        print(response)
        raise e

class Response(BaseModel):
    thought: str
    answer: str

def get_related_topics(topic : str) -> Response:
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Provide information about topics adjacent to the user's input. Output a JSON object with fields `thoughts`, and `answer`."
                + " \n`thoughts` should be a deliberation of what the user may want to know."
                + "\n`answer` should be an answer to the user's question, providing extensive information about adjacent topics in a bulleted list format."
            },
            {
                "role": "user",
                "content": "Tell me about " + topic.strip() + " and topics adjacent to it."
            },
        ],
        "response_format": {
            "type": "json_schema",
            "json_schema": {"schema": Response.model_json_schema()},
        },
    }
    response = requests.post(URL, headers=HEADERS, json=payload).json()
    raw_content = ...
    try:
        raw_content = response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        raise e

    try:
        content = json.loads(raw_content, strict=False)
        return Response(**content)
    except Exception as e:
        raise e

if __name__ == "__main__":
    print(get_related_topics("Stanford University"))