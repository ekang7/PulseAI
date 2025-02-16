import os
from db.vector_store import get_collection_stats, list_all_documents
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

def view_screenshots():
    # Check filesystem
    screenshots_dir = "screenshots"
    print("\n=== Screenshots on Disk ===")
    if os.path.exists(screenshots_dir):
        files = os.listdir(screenshots_dir)
        print(f"Number of files: {len(files)}")
        for file in files:
            if file.endswith('.png'):
                print(f"- {file}")
    else:
        print("Screenshots directory not found")
    
    # Check ChromaDB
    print("\n=== Vector Database Contents ===")
    try:
        stats = get_collection_stats("screenshots_collection")
        print(f"Number of documents: {stats.get('count', 0)}")
        
        if stats.get('count', 0) > 0:
            results = list_all_documents("screenshots_collection")
            
            print("\n=== Screenshots in Database ===")
            for i, (doc_id, doc, meta) in enumerate(zip(results["ids"], results["documents"], results["metadatas"])):
                print(f"\n--- Screenshot {i+1} ---")
                print(f"ID: {doc_id}")
                print(f"Title: {meta.get('title', 'N/A')}")
                print(f"URL: {meta.get('url', 'N/A')}")
                print(f"Timestamp: {meta.get('timestamp', 'N/A')}")
                print(f"Filename: {meta.get('filename', 'N/A')}")
                print("\nContent:")
                print(doc)
                print("-" * 80)
    except Exception as e:
        print(f"Error accessing vector database: {str(e)}")
        logger.error("Error details:", exc_info=True)

if __name__ == "__main__":
    view_screenshots()
