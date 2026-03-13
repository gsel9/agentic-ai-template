"""
App entry point.
"""
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from routers import rag_chat, weather_agent

from utils.clients import create_ai_project_client
from utils.agents import create_weather_agent
from utils import config


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """
    Lifespan function to initialize resources on startup and cleanup 
    on shutdown.
    """
    # Client for Foundry AI project
    ai_project_client = create_ai_project_client(os.getenv(config.AI_PROJ_ENDPOINT))
    # Set app state variables
    app_instance.state.aoai_client = ai_project_client.get_openai_client()
    app_instance.state.weather_agent = create_weather_agent(ai_project_client)
    # Yield control to the app
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(rag_chat.router)
app.include_router(weather_agent.router)
