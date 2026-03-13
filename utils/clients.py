"""
Instantiate client objects.
"""
from azure.identity import DefaultAzureCredential
from azure.core.credentials import AzureKeyCredential
from azure.ai.projects import AIProjectClient
from azure.search.documents import SearchClient
from openai import AzureOpenAI


def create_ai_project_client(endpoint):
    """
    Create and return an AI Project client.
    """
    return AIProjectClient(
        endpoint=endpoint,
        credential=DefaultAzureCredential()
    )


def create_chat_client(endpoint, api_key):
    """
    Create Azure OpenAI chat client.
    """
    return AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=endpoint,
        api_key=api_key
    )


def create_search_client(search_endpoint, index_name, search_key):
    """
    Create Azure search client.
    """
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_key)
    )
    return search_client


def create_embedding_client(
    openai_endpoint: str, openai_key: str
) -> AzureOpenAI:
    """
    Create an Azure OpenAI client for embeddings.
    """
    return AzureOpenAI(
        api_key=openai_key,
        api_version="2024-10-21",  # use the API version you deployed
        azure_endpoint=openai_endpoint
    )
