from db.vector_store import add_documents, query_documents, get_collection_stats

# Example documents
documents = [
    "The quick brown fox jumps over the lazy dog",
    "A fast orange fox leaps across a sleepy canine",
    "The lazy dog sleeps while the fox runs by",
    "A brown dog chases the quick fox around"
]

# Example metadata
metadata = [
    {"type": "sentence", "animal": "fox,dog"},
    {"type": "sentence", "animal": "fox,dog"},
    {"type": "sentence", "animal": "fox,dog"},
    {"type": "sentence", "animal": "fox,dog"}
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
