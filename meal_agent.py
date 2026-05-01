"""
RasaPlan Meal Agent
Main LangChain ReAct agent setup and initialization.
"""

import os
from langchain.agents import AgentType, initialize_agent
from langchain.chat_models import ChatOpenAI
from langchain.callbacks import StreamlitCallbackHandler

from agent.tools import (
    budget_calculator_tool,
    grocery_price_tool,
    nutrition_estimator_tool,
    recipe_generator_tool,
    weekly_planner_tool,
    meal_swap_tool,
    shopping_list_tool,
)
from agent.memory import create_memory, StudentProfile
from agent.prompts import SYSTEM_PROMPT


def create_agent(profile: StudentProfile, openai_api_key: str, streaming: bool = True):
    """
    Initializes the RasaPlan ReAct agent with all tools and memory.

    Args:
        profile: StudentProfile with user preferences
        openai_api_key: OpenAI API key
        streaming: Whether to enable streaming output

    Returns:
        Configured LangChain agent
    """
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7,
        openai_api_key=openai_api_key,
        streaming=streaming,
    )

    tools = [
        budget_calculator_tool,
        grocery_price_tool,
        nutrition_estimator_tool,
        recipe_generator_tool,
        weekly_planner_tool,
        meal_swap_tool,
        shopping_list_tool,
    ]

    memory = create_memory()

    system_message = SYSTEM_PROMPT.format(
        student_profile=profile.to_context_string()
    )

    agent = initialize_agent(
        tools=tools,
        llm=llm,
        agent=AgentType.CHAT_CONVERSATIONAL_REACT_DESCRIPTION,
        memory=memory,
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            "system_message": system_message,
        },
        max_iterations=6,
    )

    return agent


def run_agent_query(agent, query: str, streamlit_container=None) -> str:
    """
    Runs a query through the agent with optional Streamlit streaming.

    Args:
        agent: Initialized LangChain agent
        query: User's input query
        streamlit_container: Streamlit container for streaming output

    Returns:
        Agent's response string
    """
    try:
        if streamlit_container:
            handler = StreamlitCallbackHandler(streamlit_container)
            response = agent.run(query, callbacks=[handler])
        else:
            response = agent.run(query)
        return response
    except Exception as e:
        return f"⚠️ Agent encountered an issue: {str(e)}. Please try rephrasing your question."
