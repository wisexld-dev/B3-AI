from crewai import Agent, Task, Crew, Process, LLM
from crewai_tools import SerperDevTool
import os

llm = LLM(modal="gpt-4", temperature=0.5, api_key=os.environ.get('API_KEY'))

def main():
    crew = Crew(
        agent=[],
        tasks=[],
        process=Process.sequential,
        verbose=True
    )

    result = crew.kickoff(inputs={'topic': ''})

if __name__ == '__main__':
    main()