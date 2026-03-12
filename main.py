"""
App entry point.
"""
import os
from contextlib import asynccontextmanager
from xmlrpc import client
from fastapi import FastAPI
from routers import rag_chat, weather_agent

from utils.clients import create_ai_project_client
#from utils.agents import create_weather_agent
from utils import config


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifespan function to initialize resources on startup and cleanup 
    on shutdown.
    """
    # Initialize on startup
    app.state.ai_project_client = create_ai_project_client(os.getenv(config.AI_PROJ_ENDPOINT))
    # Yield control to the app
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(rag_chat.router)
app.include_router(weather_agent.router)
