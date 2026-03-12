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


@router.post("/weather")
def weather_api(
    query: Query,
    ai_client=Depends(get_ai_client)
):
    """
    Endpoint to execute weather agent.
    """
    agent = ai_client.agents.get_agent(os.getenv(config.WEATHER_AGENT_ID)) 

    thread = ai_client.agents.threads.create()
    print()
    print()
    print()
    print(f"Created thread, ID: {thread.id}")
    print()
    print()
    print()

    message = ai_client.agents.messages.create(
        thread_id=thread.id,
        role="user",
        content="Hi Agent926"
    )

    run = ai_client.agents.runs.create_and_process(
        thread_id=thread.id,
        agent_id=agent.id)

    if run.status == "failed":
        response_text = f"Run failed: {run.last_error}"
    else:
        response_text = ""
        messages = ai_client.agents.messages.list(thread_id=thread.id, order=ListSortOrder.ASCENDING)

        for message in messages:
            if message.text_messages:
                response_text += f"{message.role}: {message.text_messages[-1].text.value}\n"
    return {"Assistant response": response_text}

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
