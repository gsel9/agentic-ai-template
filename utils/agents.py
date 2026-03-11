"""
Instantiate agent objects.
"""
from typing import Set
from azure.ai.agents import AgentsClient
from azure.ai.agents.models import FunctionTool, ToolSet


def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"The weather in {location} is sunny and 25°C."


def create_weather_agent(
    agent_client: AgentsClient,
    model_name: str
):
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
    if not model_name:
        raise ValueError("Model name is required to create the weather agent.")

    instructions = (
        "You are a helpful assistant that can check weather."
        "When a user asks about the weather, use the `get_weather` tool "
        "with the provided city name. "
    )

    functions = FunctionTool(functions=[get_weather])

    toolset = ToolSet()
    toolset.add(functions)

    agent = agent_client.create_agent(
        model=model_name,
        name="weather-agent",
        instructions=instructions,
        toolset=toolset
    )
    
    return agent
