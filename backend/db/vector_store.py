import os
import chromadb
from chromadb.config import Settings
from typing import List, Dict, Any, Optional
from chromadb.utils import embedding_functions

# Create the directory for persistent storage
PERSIST_DIRECTORY = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")
os.makedirs(PERSIST_DIRECTORY, exist_ok=True)

# Initialize the ChromaDB client with persistent storage
client = chromadb.PersistentClient(path=PERSIST_DIRECTORY)

# Use the default embedding function from ChromaDB
default_ef = embedding_functions.DefaultEmbeddingFunction()

def get_or_create_collection(collection_name: str = "default_collection"):
    """Get an existing collection or create a new one if it doesn't exist."""
    try:
        return client.get_collection(name=collection_name)
    except chromadb.errors.InvalidCollectionException:
        return client.create_collection(
            name=collection_name,
            embedding_function=default_ef
        )

def add_documents(
    documents: List[str],
    metadata: Optional[List[Dict[str, Any]]] = None,
    ids: Optional[List[str]] = None,
    collection_name: str = "default_collection"
) -> None:
    """
    Add documents to the vector store.
    
    Args:
        documents: List of document texts to add
        metadata: Optional list of metadata dictionaries for each document
        ids: Optional list of unique IDs for each document
        collection_name: Name of the collection to add documents to
    """
    collection = get_or_create_collection(collection_name)
    
    # If no IDs provided, generate them
    if ids is None:
        ids = [str(i) for i in range(len(documents))]
    
    # If no metadata provided, use empty dicts
    if metadata is None:
        metadata = [{} for _ in documents]
    
    collection.add(
        documents=documents,
        metadatas=metadata,
        ids=ids
    )

def query_documents(
    query_text: str,
    n_results: int = 5,
    collection_name: str = "default_collection"
) -> Dict[str, Any]:
    """
    Query the vector store for similar documents.
    
    Args:
        query_text: The text to search for
        n_results: Number of results to return
        collection_name: Name of the collection to search in
        
    Returns:
        Dictionary containing the query results including documents,
        metadata, and distances
    """
    collection = get_or_create_collection(collection_name)
    
    results = collection.query(
        query_texts=[query_text],
        n_results=n_results
    )
    
    return {
        "documents": results["documents"][0],
        "metadatas": results["metadatas"][0],
        "distances": results["distances"][0],
        "ids": results["ids"][0]
    }

def delete_collection(collection_name: str) -> None:
    """Delete a collection and all its contents."""
    try:
        client.delete_collection(collection_name)
    except ValueError:
        pass  # Collection doesn't exist

def get_collection_stats(collection_name: str = "default_collection") -> Dict[str, Any]:
    """Get statistics about a collection."""
    collection = get_or_create_collection(collection_name)
    return {
        "count": collection.count(),
        "name": collection.name
    }
