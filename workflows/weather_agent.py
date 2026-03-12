from typing import Any


def query_weather_agent(
    item_id: str,
    user_id: str,
    conv_id: str,
    user_input: str,
    weather_agent: Any
):
    """
    Query the weather agent for the current weather in a given location.
    """
    #if new_user():    
    #    thread = client.threads.create()
    #    store_thread_id(user_id, thread.id)
    #else:
    #    thread = retrieve_thread_id(user_id)

    #response = timer_agent.responses.create(
    #    conversation=thread.id,
    #    input=f"What is the current weather in {user_input}?",
    #)
    #return response.choices[0].message.content
    return {"response (weather_agent)": weather_agent}


def main():
    with DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
        ) as credential, AIProjectClient(
            endpoint=endpoint, credential=credential
        ) as project_client, project_client.get_openai_client() as openai_client:

            file_obj = openai_client.files.create(
                file=open(file_path, "rb"),
                purpose="assistants",
            )

            code_tool = build_code_interpreter_tool(file_obj.id)
            func_tool = build_function_tool()

            agent = create_agent(project_client, model_name, [code_tool, func_tool])
            conversation = create_conversation(openai_client)

            chat_loop(openai_client, agent, conversation.id)

            cleanup(openai_client, conversation.id, project_client, agent)
            conversation = None
            agent = None


def create_conversation(openai_client):
    """Create a new conversation thread."""
    conversation = openai_client.conversations.create()
    log.info("Conversation created: %s", conversation.id)
    return conversation


def append_user_message(
    openai_client, conversation_id: str, text: str
) -> None:
    """Append a user message to an existing conversation."""
    openai_client.conversations.items.create(
        conversation_id=conversation_id,
        items=[{"type": "message", "role": "user", "content": text}],
    )


def request_agent_response(
    openai_client, conversation_id: str, agent
):
    """Request a response from the agent."""
    return openai_client.responses.create(
        conversation=conversation_id,
        input="",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )


def recent_snowfall(location: str) -> str:
    """
    Fetches recent snowfall totals for a given location.
    :param location: The city name.
    :return: Snowfall details as a JSON string.
    """
    mock_snow_data = {"Seattle": "0 inches", "Denver": "2 inches"}
    snow = mock_snow_data.get(location, "Data not available.")
    return json.dumps({"location": location, "snowfall": snow})