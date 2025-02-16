import os
import chromadb
from typing import List, Dict, Any, Optional
from chromadb.utils import embedding_functions
import logging
import uuid

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Create the directory for persistent storage
PERSIST_DIRECTORY = os.path.join(os.path.dirname(__file__), "..", "chroma_db")
os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

# Initialize the ChromaDB client with persistent storage
_client = None

def get_client():
    """Get or create a ChromaDB client instance."""
    global _client
    if _client is None:
        _client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)
    return _client



# Use the default embedding function from ChromaDB
default_ef = embedding_functions.DefaultEmbeddingFunction()

def get_or_create_collection(collection_name: str = "screenshots_collection"):
    """Get an existing collection or create a new one if it doesn't exist."""
    try:
        client = get_client()
        collection = client.get_collection(name=collection_name)
        logger.info(f"Retrieved existing collection: {collection_name}")
        return collection
    except chromadb.errors.InvalidCollectionException:
        logger.info(f"Creating new collection: {collection_name}")
        client = get_client()
        return client.create_collection(
            name=collection_name,
            embedding_function=default_ef
        )

def add_documents(
    documents: List[str],
    metadata: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None,
    collection_name: str = "screenshots_collection"
) -> None:
    """
    Add documents to the vector store.
    
    Args:
        documents: List of document texts to add
        metadata: Optional list of metadata dictionaries for each document
        ids: Optional list of unique IDs for each document
        collection_name: Name of the collection to add documents to
    """
    logger.info(f"Adding documents to collection {collection_name}")
    logger.info(f"Number of documents: {len(documents)}")
    logger.info(f"Document length: {[len(doc) for doc in documents]}")
    
    collection = get_or_create_collection(collection_name)
    
    # If no IDs provided, generate them
    if ids is None:
        ids = [str(uuid.uuid4()) for _ in documents]
    
    # If no metadata provided, use empty dicts
    if metadata is None:
        metadata = [{} for _ in documents]
    
    try:
        collection.add(
            documents=documents,
            metadatas=metadata,
            ids=ids
        )
        logger.info("Successfully added documents to vector store")
    except Exception as e:
        logger.error(f"Error adding documents to vector store: {str(e)}")
        raise

def query_documents(
    query_text: str,
    n_results: int = 5,
    collection_name: str = "screenshots_collection"
) -> Dict[str, Any]:
    """
    Query the vector store for similar documents.
    
    Args:
        query_text: The text to search for
        n_results: Number of results to return
        collection_name: Name of the collection to search in
        
    Returns:
        Dictionary containing the query results including documents,
        metadata, and distances. Returns empty lists if no results found.
    """
    logger.info(f"Querying collection {collection_name} for '{query_text}'")
    collection = get_or_create_collection(collection_name)

    try:
        results = collection.query(
            query_texts=[query_text],
            n_results=n_results
        )
        num_results = len(results.get('documents', [[]])[0])
        logger.info(f"Successfully queried vector store with {num_results} results")
        return {
            "documents": results.get('documents', [[]])[0],
            "metadatas": results.get('metadatas', [[]])[0],
            "distances": results.get('distances', [[]])[0],
            "ids": results.get('ids', [[]])[0]
        }
    except Exception as e:
        logger.error(f"Error querying vector store: {str(e)}")
        raise

def delete_collection(collection_name: str) -> None:
    """Delete a collection and all its contents."""
    logger.info(f"Deleting collection {collection_name}")
    try:
        client = get_client()
        client.delete_collection(collection_name)
        logger.info(f"Successfully deleted collection {collection_name}")
    except ValueError as e:
        logger.warning(f"Error deleting collection {collection_name}: {str(e)}")
        # Re-raise if it's not the "collection doesn't exist" error
        if "does not exist" not in str(e).lower():
            raise
    except Exception as e:
        logger.error(f"Unexpected error deleting collection {collection_name}: {str(e)}")
        raise

def delete_document(id: str, collection_name: str = "screenshots_collection"):
    """
    Delete a document from the vector store by ID.
    """
    logger.info(f"Deleting document with ID: {id} in collection {collection_name}")
    collection = get_or_create_collection(collection_name)
    collection.delete(ids=[id])
    logger.info(f"Document {id} deleted successfully.")


def update_document(
    id: str,
    new_content: str,
    new_metadata: dict,
    collection_name: str = "screenshots_collection"
):
    """
    Update a document in the vector store by ID using ChromaDB's upsert functionality.
    This ensures atomic updates without potential data loss.
    """
    logger.info(f"Updating document with ID: {id} in collection {collection_name}")
    collection = get_or_create_collection(collection_name)

    try:
        collection.upsert(
            documents=[new_content],
            metadatas=[new_metadata],
            ids=[id]
        )
        logger.info(f"Document {id} updated successfully.")
    except Exception as e:
        logger.error(f"Error updating document {id}: {str(e)}")
        raise

def get_collection_stats(collection_name: str = "screenshots_collection") -> Dict[str, Any]:
    """Get statistics about a collection."""
    logger.info(f"Getting stats for collection {collection_name}")
    collection = get_or_create_collection(collection_name)
    try:
        stats = {
            "count": collection.count(),
            "name": collection.name
        }
        logger.info(f"Successfully retrieved stats for collection {collection_name}")
        return stats
    except Exception as e:
        logger.error(f"Error getting stats for collection {collection_name}: {str(e)}")
        raise

def list_all_documents(collection_name: str = "screenshots_collection") -> Dict[str, Any]:
    """List all documents in a collection with their IDs and metadata."""
    logger.info(f"Listing all documents in collection {collection_name}")
    collection = get_or_create_collection(collection_name)
    try:
        # Get all documents
        results = collection.get()
        
        return {
            "ids": results["ids"],
            "documents": results["documents"],
            "metadatas": results["metadatas"]
        }
    except Exception as e:
        logger.error(f"Error listing documents: {str(e)}")
        raise
