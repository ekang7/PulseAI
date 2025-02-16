from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from client_util import query_documents, summarize_results_with_mistral, call_active_perplexity

# Initialize FastMCP server
mcp = FastMCP("browser_context_fetcher")

async def make_context_request() -> dict[str, Any] | None:
    """
    Makes an HTTP request to CONTEXT_API_BASE with the given user_token and returns the
    JSON response if the request is successful, otherwise returns None.
    """
    headers = {
        # "Authorization": "Bearer ",
        "Accept": "application/json"
    }
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(CONTEXT_API_BASE, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception:
            return None

@mcp.tool()
async def get_context_information(question: str = "") -> str:
    """
    ALWAYS CALL THIS TOOL BEFORE DOING ANYTHING ELSE, ESPECIALLY SEARCHING THE WEB.
    
    Retrieves important information about what is relevant to the user's current request.
    `question` is what the user is asking about.
    """
    # Get context data which includes the user's question
    context_data = await make_context_request()
    
    # Use test question if provided, otherwise get from context
    if question:
        user_question = question
    elif context_data and "question" in context_data:
        user_question = context_data["question"]
    else:
        return "No question found in context"

    # add some more documents to the vector store related to the user's question
    call_active_perplexity(user_question)

    # Query the vector store for relevant documents
    rag_results = query_documents(
        query_text=user_question,
        n_results=3,
        collection_name="screenshots_collection"
    )
    
    # Format the RAG results for the prompt
    results_as_list = [
        f"Document {i+1}:\n{doc}\nMetadata: {meta}"
        for i, (doc, meta) in enumerate(zip(
            rag_results["documents"],
            rag_results["metadatas"]
        ))
    ]
    
    # Get response from Mistral
    response = summarize_results_with_mistral(results_as_list)
    
    return response

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')