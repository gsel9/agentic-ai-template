"""
"""
from typing import List, Dict, Any, Union
from azure.search.documents.models import VectorizedQuery


# TODO: see https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/README.md
def run_vector_search(
    search_client: Any,
    embedding_client: Any,
    embedding_model: Union[str, None],
    query: str
) -> str:
    """
    Executes a vector search against Azure AI Search.

    Returns the top k results.
    """
    # Embedding for the user query
    embedding = embedding_client.embeddings.create(
        model=embedding_model,
        input=query
    ).data[0].embedding

    # Create vector query
    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=5,  # Number of similar documents to return
        fields="text_vector"    # Name of the vector field in your index
    )
    
    # Execute vector search. You can also add "search_text=query" for HYBRID search (kwarg + vector)
    results_iter = search_client.search(
        search_text=None,  # None for pure vector search
        vector_queries=[vector_query],
        top=5
    )
    
    # Collect results and apply threshold
    results: List[Dict[str, Any]] = []
    for doc in results_iter:
        if doc.get("@search.score", 0.0) < 0.6:
            continue

        results.append(doc["chunk"])
        
    return "\n".join(results)
