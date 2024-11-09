from crewai import Agent
from crewai_tools import SerperDevTool
from main import llm

baseAgent = Agent(
    role="Base Agent",
    goal="", # Objetivo do Agent
    backstory="", # História do Agent (ex: Você é um trader renomado...)
    tools=[SerperDevTool()],
    llm=llm
)