"""
App router for timer agent.
"""
from time import time
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from workflows.weather_agent import query_weather_agent
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


def get_client(request: Request):
    """
    Dependency to get the agent client from app state.
    FastAPI injects a Request object when the function is used as a dependency.
    """
    return request.app.state.ai_project_client


@router.post("/weather")
def weather_api(
    query: Query,
    #weather_agent=Depends(get_weather_agent)
    client=Depends(get_client)
): # -> Dict[str, Any]:
    """
    Endpoint to execute weather agent.

    FastAPI will:
        Call get_agent_client(request) automatically before calling weather_api
        Inject the returned value into the agent_client parameter
        Pass it to weather_api() just like a normal function argument
    """    
    thread = client.agents.threads.create()
    thread_id = thread.id
    # 2. Add a user message to the thread
    client.agents.messages.create(
        thread_id=thread_id,
        role="user",
        content="Explain retrieval augmented generation."
    )
    # 3. Start a run using your existing Foundry agent
    run = client.agents.runs.create(
        thread_id=thread_id,
        agent_id=os.getenv(config.WEATHER_AGENT_ID)
    )
    # 4. Poll until the run completes
    while True:
        status = client.agents.runs.retrieve(
            thread_id=thread_id,
            run_id=run.id
        )
        if status.status in ("completed", "failed", "cancelled"):
            break
        time.sleep(0.5)
    
    # 5. Retrieve the assistant’s output
    messages = client.agents.messages.list(thread_id=thread_id)

    assistant_messages = [
        m for m in messages.data if m.role == "assistant"
    ]

    last_message = assistant_messages[-1]

    response_text = ""
    for block in last_message.content:
        if block.type == "output_text":
            response_text += block.text

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
