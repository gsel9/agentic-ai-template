from typing import Any


def query_weather_agent(
    query: Any,
    conversation_id: str,
    aoai_client: Any,
    weather_agent: Any
) -> str:
    """
    Query the weather agent for the current weather in a given location.
    """
    # Add user message
    append_user_message(
        aoai_client, conversation_id, query.user_input
    )
    # Request agent response
    response = request_agent_response(
        aoai_client, conversation_id, query.user_input, weather_agent
    )
    # Return response text
    return response.output[0].content[0].text


def append_user_message(
    aoai_client, conversation_id: str, text: str
) -> None:
    """Append a user message to an existing conversation."""
    aoai_client.conversations.items.create(
        conversation_id=conversation_id,
        items=[{"type": "message", "role": "user", "content": text}],
    )


def request_agent_response(
    aoai_client, conversation_id: str, user_input: str, agent: Any
):
    """Request a response from the agent."""
    return aoai_client.responses.create(
        conversation=conversation_id,
        input=[{
            "role": "user",
            "content": [{
                "type": "input_text",
                "text": user_input
            }]
        }],
        extra_body={
            "agent_reference": {
                "type": "agent_reference",
                "name": agent.name
            }
        }
    )
