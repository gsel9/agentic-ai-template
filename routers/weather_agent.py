"""
App router for weather agent.
"""
from fastapi import APIRouter, Depends, HTTPException, Request
from routers._datamodels import Query
from workflows.weather_agent import query_weather_agent

router = APIRouter()


def get_weather_agent(request: Request):
    """
    Dependency to get the agent client from app state.
    FastAPI injects a Request object when the function is used as a dependency.
    """
    return request.app.state.weather_agent


def get_aoai_client(request: Request):
    """
    Dependency to get the agent client from app state.
    FastAPI injects a Request object when the function is used as a dependency.
    """
    return request.app.state.aoai_client


@router.post("/weather")
def weather_api(
    query: Query,
    weather_agent=Depends(get_weather_agent),
    aoai_client=Depends(get_aoai_client)
):
    """
    Endpoint to execute weather agent.
    """
    # NOTE TEMP: Create new conversation each time -> should be tied to session/user ID
    conversation = aoai_client.conversations.create()
    #if new_user():
    #    thread = client.threads.create()
    #    store_thread_id(user_id, thread.id)
    #else:
    #    thread = retrieve_thread_id(user_id)

    try:
        answer = query_weather_agent(
            query, conversation.id, aoai_client, weather_agent
        )
        return {"answer": answer}
    except Exception as exc:
        # log.exception("ask_api failed")  # add logging as needed
        raise HTTPException(status_code=500, detail=str(exc))
