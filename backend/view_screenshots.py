import os
from db.vector_store import get_collection_stats, query_documents

def view_screenshots():    
    # Check ChromaDB
    print("\n=== Vector Database Contents ===")
    try:
        stats = get_collection_stats("screenshots_collection")
        print(f"Number of documents: {stats.get('count', 0)}")
        
        if stats.get('count', 0) > 0:
            results = query_documents(
                query_text="Show me all screenshots",
                n_results=100,
                collection_name="screenshots_collection"
            )
            
            print("\n=== Screenshots in Database ===")
            for i, (doc, meta) in enumerate(zip(results["documents"], results["metadatas"])):
                print(f"\n--- Screenshot {i+1} ---")
                print(f"Title: {meta.get('title', 'N/A')}")
                print(f"URL: {meta.get('url', 'N/A')}")
                print(f"Timestamp: {meta.get('timestamp', 'N/A')}")
                print(f"Filename: {meta.get('filename', 'N/A')}")
                print("\nContent:")
                # Print full content without truncation
                print(doc[:2000] + "..." if len(doc) > 500 else doc)
                print("-" * 80)
    except Exception as e:
        print(f"Error accessing vector database: {str(e)}")

if __name__ == "__main__":
    view_screenshots()
