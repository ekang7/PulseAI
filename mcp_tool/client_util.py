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

rag_results = query_documents(
        query_text="Hello?",
        n_results=3,
        collection_name="screenshots_collection"
    )
# Format the RAG results for the prompt
formatted_results = [
    f"Document {i+1}:\n{doc}\nMetadata: {meta}"
    for i, (doc, meta) in enumerate(zip(
        rag_results["documents"],
        rag_results["metadatas"]
    ))
]