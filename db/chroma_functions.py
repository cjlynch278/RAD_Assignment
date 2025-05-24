from chromadb import Client
from chromadb.config import Settings

import chromadb

from chromadb.utils import embedding_functions

def chroma_setup(simulated_cves):
    """
    Initializes a ChromaDB collection and populates it with CVE data.

    Args:
        simulated_cves (list of dict): List of CVE dictionaries, each with at least 'id' and 'description' keys.

    Returns:
        chromadb.Collection: The populated ChromaDB collection.
    """

    # My preferred distance function is cosine, but you can choose others like "euclidean" or "dot"
    # Cosine distance ranges from -1 (opposite) to 1 (exact match).
    client = chromadb.Client()
    #client.delete_collection("cves")  # Ensure a clean start by deleting any existing collection with the same name
    
    embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(model_name="all-MiniLM-L6-v2")
    # Check if collection already exists

    cve_collection = client.create_collection(
        name="cves",
        embedding_function=embedding_function,
        metadata={"hnsw:space": "cosine"}  # This sets the distance metric to cosine

    )

    for cve in simulated_cves:
        # Each document must have a unique id and some content
        cve_collection.add(
            documents=[cve['description']],
            ids=[cve['cve_id']],
           # metadatas=[{k: v for k, v in cve.items() if k not in ['id', 'description']}]
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
def create_collection(client):
    collection = client.create_collection("cve_data")
    return collection

def initialize_database():
    client = setup_chroma_db()
    collection = create_collection(client)
    return collection

def get_all_cves():
    return self.collection.get(
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



def query_collection( query_text, collection, n_results=5):
    """Queries the ChromaDB collection with a given text.
    setting n_results to 5 returns the top 5 results which should be sufficient for most queries, and not overwhelm the llm
    """
    
    result = collection.query(
        query_texts=[query_text],
        n_results=5,
        include=["documents", "metadatas", "embeddings","distances"]
    )
    return result if result["ids"] else None