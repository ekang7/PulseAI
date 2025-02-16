"""
Client for interacting with the Perplexity AI API. This module provides functions to perform
searches and get related topics using Perplexity's language models.
"""

import requests
import simplejson as json
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import asyncio
from typing import List

load_dotenv()
PERPLEXITY_API_KEY = os.getenv("PERPLEXITY_API_KEY")


URL = "https://api.perplexity.ai/chat/completions"
HEADERS = {"Authorization": "Bearer " + PERPLEXITY_API_KEY}
MODEL = "sonar"

class Response(BaseModel):
    """
    Response model for Perplexity API responses.
    
    Attributes:
        thoughts (str): The model's thought process or deliberation
        answer (str): The final answer or response to the query
    """
    thoughts: str
    answer: str

def get_search_response(user_prompt : str) -> Response:
    """
    Performs a search query using Perplexity AI and returns a structured response.
    
    Args:
        user_prompt (str): The user's search query or question
        
    Returns:
        Response: A Response object containing the model's thoughts and answer
        
    Raises:
        Exception: If there's an error in API response or JSON parsing
    """  
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


def get_related_topics(topic : str) -> Response:
    """
    Retrieves information about topics related to the input topic.
    
    Args:
        topic (str): The main topic to find related information about
        
    Returns:
        Response: A Response object containing thoughts and a bulleted list of related topics
        
    Raises:
        Exception: If there's an error in API response or JSON parsing
    """
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Provide in-depth information about the user's input and exactly 3 topics adjacent to it. Output a JSON object with fields `thoughts`, and `answer`."
                + " \n`thoughts` should be a discussion with yourself about what the user may want to know."
                + "\n`answer` should be an answer to the user's question, providing extensive information about adjacent topics in a bulleted list format. Each topic should have at least three sentences."
                + "\nIf the user is asking about something related to programming, make sure to include code examples and explanations throughout your response."
            },
            {
                "role": "user",
                "content": "Tell me about " + topic.strip() + " and 3 topics adjacent to it."
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

def get_related_topics_with_other_topics(topic : str, other_topics : List[str]) -> Response:
    prompted_topics = ""
    for i in range(len(other_topics)):
        prompted_topics += "- " + other_topics[i] + "\n"
    payload = {
        "model": MODEL,
        "messages": [
            {
                "role": "system",
                "content": "Provide in-depth information about the user's input and exactly 3 topics adjacent to it. Output a JSON object with fields `thoughts`, and `answer`."
                + " \n`thoughts` should be a discussion with yourself about what the user may want to know."
                + "\n`answer` should be an answer to the user's question, providing extensive information about adjacent topics in a bulleted list format. Each topic should have at least three sentences."
                + "\nIf the user is asking about something related to programming, make sure to include code examples and explanations throughout your response."
            },
            {
                "role": "user",
                "content": "Tell me about " + topic.strip() + ". Then, tell me about 3 topics relevant to it. Some potentially related topics we are aware of are:\n" + prompted_topics
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
        print(content["answer"])
        return Response(**content)
    except Exception as e:
        raise e