from chromadb import Client
from chromadb.config import Settings

import chromadb

from chromadb.utils import embedding_functions

def chroma_setup(simulated_cves):
    """
    Initializes a persistent ChromaDB collection and populates it with CVE data.

    Args:
        simulated_cves (list of dict): List of CVE dictionaries, each with at least 'id' and 'description' keys.

    Returns:
        chromadb.Collection: The populated ChromaDB collection.
    """
    print("Setting up")
    # Initialize the persistent ChromaDB client
    print("Creating client with persistence")
    client = chromadb.PersistentClient(path="./data/chroma_db") #hardcoded path for now, can be changed later

    # Embedding function for converting text to embeddings
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")

    # Check if the collection already exists
    existing_collections = client.list_collections()
    if "cves" in [col.name for col in existing_collections]:
        # Retrieve the existing collection
        print("Collection 'cves' already exists. Retrieving it.")
        cve_collection = client.get_collection(
            name="cves",
            embedding_function=embedding_function,
        )
    else:
        print("Collection 'cves' does not exist. Creating a new one.")
        print("Creating Collection")
        cve_collection = client.create_collection(
            name="cves",
            embedding_function=embedding_function,
            metadata={"hnsw:space": "cosine"}  # To parameterize
        )

        print("Adding CVEs")
        for cve in simulated_cves:
            # Each document must have a unique id and some content
            print(f"Adding CVE {cve}")
            cve_collection.add(
                documents=[cve['description']],
                ids=[cve['cve_id']],
                metadatas=[{
                    # Quick hack to turn given list into string.
                    "affected_software": ", ".join(cve.get("affected_software", [])),
                    "cvss_score": cve.get("cvss_score", None)
                }]
            )

    return cve_collection

def delete_collection(client, collection_name):
    """
    Deletes a ChromaDB collection by name.

    Args:
        client (chromadb.Client): The ChromaDB client instance.
        collection_name (str): The name of the collection to delete.
    """
    try:
        client.delete_collection(collection_name)
        print(f"Collection '{collection_name}' deleted successfully.")
    except Exception as e:
        print(f"Error deleting collection '{collection_name}': {e}")
def get_collection(client, collection_name):
    """
    Retrieves a ChromaDB collection by name.

    Args:
        client (chromadb.Client): The ChromaDB client instance.
        collection_name (str): The name of the collection to retrieve.

    Returns:
        chromadb.Collection: The retrieved collection.
    """
    try:
        collection = client.get_collection(name=collection_name)
        print(f"Collection '{collection_name}' retrieved successfully.")
        return collection
    except Exception as e:
        print(f"Error retrieving collection '{collection_name}': {e}")
        return None
def create_collection(client):
    collection = client.create_collection("cve_data")
    return collection

def initialize_database():
    client = setup_chroma_db()
    collection = create_collection(client)
    return collection

def get_all_cves():
    return collection.get(
        include=["documents", "metadatas", "embeddings"])

def get_cve_by_id(cve_id):
    """Retrieves a CVE from ChromaDB by its unique ID."""
    result = self.collection.get(ids=[str(cve_id)], include=["documents", "metadatas", "embeddings"])
    return result if result["ids"] else None

def get_cve_by_name(cve_name):
    """Retrieves CVEs by name (exact match)."""
    results = self.collection.query(
        query_texts=[cve_name], n_results=5, include=["documents", "metadatas", "embeddings"]
    )
    return results if results["ids"] else None


# Leaving n_results parameter for potential debugging or future use
def query_collection( query_text, collection, n_results=5):
    """Queries the ChromaDB collection with a given text.
    setting n_results to 5 returns the top 5 results which should be sufficient for most queries, and not overwhelm the llm
    """
    
    result = collection.query(
        query_texts=[query_text],
        n_results=n_results,
        include=["documents", "metadatas", "distances"]
    )
    return result if result["ids"] else None