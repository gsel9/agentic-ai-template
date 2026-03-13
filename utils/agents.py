"""
Instantiate agent objects.
"""
import os

from azure.ai.projects.models import PromptAgentDefinition
from utils import config


def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"The weather in {location} is sunny and 25°C."


def create_weather_agent(ai_project_client):
    """
    Create and return the weather agent with a callable tool `recent_snowfall`.

    Parameters
    ----------
    agent_client : AgentsClient
        Initialized Agents client (stored on app.state.agent_client).
    model_name : str
        The model deployment name (e.g., from env `WEATHER_AGENT_MODEL`).
    instructions : Optional[str]
        Optional system prompt for the agent.

    Returns
    -------
    Agent
        The created agent object.
    """ 
    instructions = (
        "You are a helpful assistant that can answer weather questions."
        #"When a user asks about the weather, use the `get_weather` tool "
        #"with the provided city name. "
    )
    agent = ai_project_client.agents.create_version(
        agent_name="weather-agent",
        definition=PromptAgentDefinition(
            model=os.getenv(config.CHAT_MODEL),
            instructions=instructions
        )
    )
    return agent
