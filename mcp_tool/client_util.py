import requests
from typing import List, Any, Dict

BACKEND_URL = "http://localhost:8000"

def query_documents(
    query_text: str,
    n_results: int = 5,
    collection_name: str = "screenshots_collection"
) -> Dict[str, Any]:
    response = requests.post(BACKEND_URL + "/api/query_documents", json={
        "query_text": query_text,
        "n_results": n_results,
        "collection_name": collection_name
    })
    return response.json()

def summarize_results_with_mistral(
    sources : List[Any]
) -> str:
    response = requests.post(BACKEND_URL + "/api/collective_summary", json={
        "sources": sources
    })
    return response.json()["summary"]


def call_active_perplexity(
    question: str
) -> None:
    requests.post(BACKEND_URL + "/api/call_active_perplexity", json={
        "question": question
    })
    return None