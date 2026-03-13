"""
App router for timer agent.
"""
from time import time
from typing import Dict, Any
from urllib import response
from fastapi import APIRouter, Depends, HTTPException, Request
from workflows.weather_agent import query_weather_agent
from azure.ai.agents.models import ListSortOrder
from routers._datamodels import Query
import os 
from utils import config

router = APIRouter()


def get_weather_agent(request: Request):
    """
    Dependency to get the agent client from app state.
    FastAPI injects a Request object when the function is used as a dependency.
    """
    return request.app.state.weather_agent


def get_ai_client(request: Request):
    """
    Dependency to get the agent client from app state.
    FastAPI injects a Request object when the function is used as a dependency.
    """
    return request.app.state.ai_project_client


from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition


@router.post("/weather")
def weather_api(
    query: Query,
    #ai_client=Depends(get_ai_client)
):
    """
    Endpoint to execute weather agent.
    """
    project_client = AIProjectClient(
        endpoint=os.getenv(config.AI_PROJ_ENDPOINT), 
        credential=DefaultAzureCredential()
    )
    # Get OpenAI client
    openai_client = project_client.get_openai_client()
    # Create agent
    agent = project_client.agents.create_version(
        agent_name="support-agent",
        definition=PromptAgentDefinition(
            model=os.getenv(config.CHAT_MODEL),
            instructions="You are a helpful assistant."
        ),
    )
    # Create conversation
    conversation = openai_client.conversations.create()
    # Add user message to conversation
    openai_client.conversations.items.create(
        conversation_id=conversation.id,
        items=[{"type": "message", "role": "user", "content": query.user_input}],
    )
    # Get response
    response = openai_client.responses.create(
        conversation=conversation.id,
        input="",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
    """
    try:
        answer = query_weather_agent(
            query.item_id,
            query.user_id,
            query.conv_id,
            query.user_input,
            weather_agent,  # pass down weather agent client from app.state
        )
        return {"answer": answer}
    except Exception as exc:
        # log.exception("ask_api failed")  # add logging as needed
        raise HTTPException(status_code=500, detail=str(exc))
    """
