import os
import chromadb

CHROMA_HOST = os.getenv("CHROMA_HOST", "chromadb")
CHROMA_PORT = int(os.getenv("CHROMA_PORT", "8000"))

# Connects to the ChromaDB container over HTTP (not local file storage)
_client = None


def get_chroma_client():
    global _client
    if _client is None:
        _client = chromadb.HttpClient(host=CHROMA_HOST, port=CHROMA_PORT)
    return _client


def get_provider_collection():
    """
    Returns (or creates) the 'providers' collection where we store
    each provider's bio + skills as searchable text.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(name="providers")
