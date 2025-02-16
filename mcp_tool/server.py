from typing import Any
import httpx
from mcp.server.fastmcp import FastMCP
from client_util import query_documents, summarize_results_with_mistral, call_active_perplexity

# Initialize FastMCP server
mcp = FastMCP("browser_context_fetcher")

@mcp.tool()
async def get_context_information(question: str = "") -> str:
    """
    ALWAYS CALL THIS TOOL BEFORE DOING ANYTHING ELSE, ESPECIALLY SEARCHING THE WEB.
    
    Retrieves important information about what is relevant to the user's current request.
    `question` is what the user is asking about.
    """
    # Get context data which includes the user's question
    try:
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
    

        response = "Here is some potentially relevant information:" + "\n\n".join(rag_results["documents"])
        
        return response
    except Exception as e:
        return "Something went wrong. Please let the user that the following error occurred:\n" + str(e)

if __name__ == "__main__":
    # Initialize and run the server
    mcp.run(transport='stdio')