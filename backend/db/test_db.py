from db.vector_store import add_documents, query_documents, get_collection_stats, delete_collection

# First, let's clean up any existing collection
print("Cleaning up existing collection...")
delete_collection("test_collection")

# Test data
documents = [
    "Python is a high-level programming language",
    "JavaScript is commonly used for web development",
    "Machine learning is a subset of artificial intelligence",
    "Neural networks are used in deep learning"
]

# Add some metadata
metadata = [
    {"topic": "programming", "language": "Python"},
    {"topic": "programming", "language": "JavaScript"},
    {"topic": "AI", "field": "machine_learning"},
    {"topic": "AI", "field": "deep_learning"}
]

print("\nAdding documents to the database...")
add_documents(
    documents=documents,
    metadata=metadata,
    collection_name="test_collection"
)

# Check if documents were added
stats = get_collection_stats("test_collection")
print(f"\nCollection stats: {stats}")

# Try some queries
queries = [
    "What programming languages are mentioned?",
    "Tell me about artificial intelligence",
    "web development information"
]

print("\nTesting queries...")
for query in queries:
    print(f"\nQuery: '{query}'")
    results = query_documents(query, n_results=2, collection_name="test_collection")
    
    for i, (doc, meta, dist) in enumerate(zip(
        results["documents"],
        results["metadatas"],
        results["distances"]
    )):
        print(f"\nResult {i+1}:")
        print(f"Document: {doc}")
        print(f"Metadata: {meta}")
        print(f"Distance: {dist:.4f}")
