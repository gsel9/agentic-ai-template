"""
Interactive CLI-driven chat loop.
"""
import logging
from typing import Any, List, Union

log = logging.getLogger(__name__)


def _output_text(response: Any) -> str:
    """Extract plain output text from a response."""
    return response.choices[0].message.content


def _finish_reason(response: Any) -> str:
    """Extract finish reason from a response."""
    return response.choices[0].finish_reason


def chat_turn(
    chat_client: Any,
    chat_model: Union[str, None],
    messages: List[dict]
) -> Union[str, None]:
    """
    Single chat turn: call model once and return the answer
    """
    try:
        response = chat_client.chat.completions.create(
            model=chat_model, messages=messages
        )
    except Exception as exc:
        log.error("Error requesting response: %s", exc)
        # Remove the last user message to avoid poisoning the chat history
        messages.pop()
        return None

    if _finish_reason(response) != "stop":
        log.error("Agent error: %s", getattr(response, "error", "<no details>"))
        return None

    return _output_text(response)
