import asyncio
from server import get_necessary_information
from backend.db.vector_store import add_documents, delete_collection

# Sample documents about different programming topics
documents = [
    "Python is a high-level programming language known for its simplicity and readability. It's widely used in data science, web development, and AI.",
    "JavaScript is the primary language for web development, enabling interactive web pages and running both in browsers and on servers via Node.js.",
    "React is a JavaScript library for building user interfaces, particularly single-page applications. It was developed by Facebook.",
    "Docker is a platform for developing, shipping, and running applications in containers, making it easier to deploy software consistently.",
    "Git is a distributed version control system that helps track changes in source code during software development.",
]

metadata = [
    {"topic": "programming", "language": "Python", "category": "language"},
    {"topic": "web", "language": "JavaScript", "category": "language"},
    {"topic": "web", "framework": "React", "category": "framework"},
    {"topic": "devops", "tool": "Docker", "category": "platform"},
    {"topic": "devops", "tool": "Git", "category": "tool"},
]

async def test_mcp_tool():
    # First, set up our test data in ChromaDB
    print("1. Setting up test data in ChromaDB...")
    delete_collection("default_collection")
    add_documents(
        documents=documents,
        metadata=metadata,
        collection_name="default_collection"
    )
    
    # Test queries that would normally come from Codeium
    test_queries = [
        "What are the main web development technologies?",
        "Tell me about version control and deployment tools",
        "What programming languages are good for AI and data science?"
    ]
    
    for query in test_queries:
        print(f"\n\nTesting MCP tool with query: '{query}'")
        print("-" * 50)
        
        # Call the MCP tool's get_necessary_information function with test query
        response = await get_necessary_information(test_question=query)
        
        print("\nMCP Tool Response:")
        print("-" * 50)
        print(response)
        print("-" * 50)

def main():
    asyncio.run(test_mcp_tool())

if __name__ == "__main__":
    main()
