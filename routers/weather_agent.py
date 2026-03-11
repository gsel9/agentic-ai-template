"""
App router for timer agent.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends, HTTPException, Request
from workflows.weather_agent import query_weather_agent
from routers._datamodels import Query

router = APIRouter()


def get_weather_agent(request: Request):
    """
    Dependency to get the agent client from app state.
    FastAPI injects a Request object when the function is used as a dependency.
    """
    return request.app.state.weather_agent


@router.post("/weather")
def weather_api(
    query: Query,
    weather_agent=Depends(get_weather_agent)
) -> Dict[str, Any]:
    """
    Endpoint to execute weather agent.

    FastAPI will:
        Call get_agent_client(request) automatically before calling weather_api
        Inject the returned value into the agent_client parameter
        Pass it to weather_api() just like a normal function argument
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
