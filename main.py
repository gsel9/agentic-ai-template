"""
App entry point.
"""
import os 
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import rag_chat, weather_agent

from utils.clients import create_agent_client
from utils.agents import create_weather_agent
from utils import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to initialize resources on startup and cleanup 
    on shutdown.
    """
    # Initialize on startup
    app.state.agent_client = create_agent_client(
        os.getenv(config.AGENT_ENDPOINT)
    )
    app.state.weather_agent = create_weather_agent(
        app.state.agent_client, os.getenv(config.WEATHER_AGENT_MODEL)
    )
    # Yield control to the app
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(rag_chat.router)
app.include_router(weather_agent.router)
