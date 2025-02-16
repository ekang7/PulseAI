from db.vector_store import add_documents, query_documents, get_collection_stats

# Example documents
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

def main():
    # Add documents to the vector store
    print("Adding documents to vector store...")
    add_documents(documents, metadata=metadata)
    
    # Get collection statistics
    stats = get_collection_stats()
    print(f"\nCollection stats: {stats}")
    
    # Perform a query
    query = "fox jumping over dog"
    print(f"\nQuerying for: '{query}'")
    results = query_documents(query)
    
    # Print results
    print("\nResults:")
    for doc, meta, dist in zip(results["documents"], 
                             results["metadatas"], 
                             results["distances"]):
        print(f"\nDocument: {doc}")
        print(f"Metadata: {meta}")
        print(f"Distance: {dist}")

if __name__ == "__main__":
    main()
