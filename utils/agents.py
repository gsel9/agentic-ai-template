"""
Instantiate agent objects.

###   -*- Add search tool to Agent -*-   ###
###### 
from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import (
    AgentDefinition,
    AzureAISearchTool,
    AzureAISearchToolResource,
    AISearchIndexResource,
    AzureAISearchQueryType,
)
from azure.identity import DefaultAzureCredential
import os

# Initialize the Foundry project client
project = AIProjectClient(
    endpoint=os.environ["AZURE_AI_PROJECT_ENDPOINT"],
    credential=DefaultAzureCredential()
)

# Configure your Azure AI Search tool
search_tool = AzureAISearchTool(
    azure_ai_search=AzureAISearchToolResource(
        indexes=[
            AISearchIndexResource(
                project_connection_id=os.environ["AI_SEARCH_PROJECT_CONNECTION_ID"],
                index_name=os.environ["AI_SEARCH_INDEX_NAME"],
                query_type=AzureAISearchQueryType.SIMPLE
            )
        ]
    )
)

# Create or update your agent to include RAG
agent = project.agents.create_version(
    agent_name="rag-agent",
    definition=AgentDefinition(
        model=os.environ["AZURE_AI_MODEL_DEPLOYMENT_NAME"],
        instructions="Use the search tool to answer questions using RAG.",
        tools=[search_tool]
    )
)

print("Agent created with Search-enabled RAG:", agent)
"""
from typing import Set
#from azure.ai.projects import AIProjectClient AgentsOperations 
from azure.ai.agents.models import FunctionTool, ToolSet
from openai import project

from azure.ai.projects.models import PromptAgentDefinition


def get_weather(location: str) -> str:
    """Get the current weather for a location."""
    return f"The weather in {location} is sunny and 25°C."


import os
from azure.ai.agents import AgentsClient
from azure.identity import DefaultAzureCredential


def create_weather_agent(
    project_client, agent_id #: AIProjectClient, agent_id: str
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
    instructions = (
        "You are a helpful assistant that can check weather."
        "When a user asks about the weather, use the `get_weather` tool "
        "with the provided city name. "
    )
    """
    functions = FunctionTool(functions=[get_weather])

    toolset = ToolSet()
    toolset.add(functions)

    agent = agent_client.create_agent(
        model=model_name,
        name="weather-agent",
        instructions=instructions,
        #toolset=toolset
    )
    """
    
    agents_client = AgentsClient(
        endpoint=os.getenv("AZURE_AI_PROJECT_ENDPOINT"),
        credential=DefaultAzureCredential()
    )

    agent = project_client.agents.create_version(
        agent_name="MyAgent",
        definition=PromptAgentDefinition(
            model="gpt-4o",
            instructions="You are a helpful assistant that answers general questions.",
        ),
    )
    return agent
