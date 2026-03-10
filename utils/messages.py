"""
"""
from typing import List, Dict


def chat_instructions() -> List[Dict[str, str]]:
    """Initialize prompt with system message."""
    return [{
        "role": "system",
        # System message for travel-related chat solution
        "content": (
            "You are a travel assitant that provides information"
            " on travel services available from Margie's travel."
        )
    }]


def create_context_message(messages: List[Dict], context: str) -> List:
    """
    Add retrieved context to (local) message history.
    """
    system_context_msg = {
        "role": "system",
        "content": (
            "Here is relevant information from your knowledge base:"
            f"\n\n{context}\n\n"
            "Use it to answer the user query."
        )
    }
    messages.append(system_context_msg)

    return messages


def build_messages(conversation_history, user_query, rag_context):
    """
    TODO
    """
    messages = []

    messages.append({
        "role": "system",
        "content": (
            "You are a helpful assistant."
            "Use provided context when relevant."
        )
    })

    # Add conversation history from Cosmos DB
    messages.extend(conversation_history)

    # Add retrieved RAG context
    if rag_context:
        messages.append({
            "role": "system",
            "content": f"Relevant retrieved context:\n{rag_context}"
        })

    # Add the user's new question
    messages.append({
        "role": "user",
        "content": user_query
    })

    return messages
