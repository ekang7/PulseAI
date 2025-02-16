from db.vector_store import add_documents, delete_collection

# Sets up example DB

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

print("Setting up test data in ChromaDB...")
delete_collection("default_collection")
add_documents(
    documents=documents,
    metadata=metadata,
    collection_name="default_collection"
)
print("Done! Test data has been loaded into ChromaDB.")
