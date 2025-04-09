#!/usr/bin/env python3
"""Example script demonstrating how to use the CrewAI adapter for uAgents."""

import os
from crewai import Crew, Agent, Task
from langchain_openai import ChatOpenAI
from uagents.experimental.adapters.crewai import CrewAIRegisterTool
#from tools import CrewAIRegisterTool

def main():
    """Main function to demonstrate CrewAI adapter."""
    
    # Load API key from environment
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("Error: AGENTVERSE_API_KEY not found in environment")
        return
    
    # Create an LLM
    llm = ChatOpenAI(
        model="gpt-4o",
        temperature=0.7)
    
    # Create CrewAI agents
    researcher = Agent(
        role="Senior Research Analyst",
        goal="Uncover valuable insights on technology trends",
        backstory="You're a technology research analyst with expertise in identifying emerging trends.",
        verbose=True,
        llm=llm
    )
    
    writer = Agent(
        role="Technical Writer",
        goal="Write clear and concise reports on technology trends",
        backstory="You're a skilled technical writer who can explain complex topics in simple terms.",
        verbose=True,
        llm=llm
    )
    
    # Create tasks
    research_task = Task(
        description="Research the latest trends in artificial intelligence and machine learning.",
        expected_output="A comprehensive analysis of the latest AI and ML trends with specific examples and data points.",
        agent=researcher
    )
    
    writing_task = Task(
        description="Write a report summarizing the findings from the research task.",
        expected_output="A well-structured report that clearly explains the AI and ML trends in accessible language.",
        agent=writer,
        dependencies=[research_task]
    )
    
    # Create crew
    tech_trends_crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, writing_task],
        verbose=True
    )
    
    # Create tool for registering the crew with Agentverse
    register_tool = CrewAIRegisterTool()
    
    # Register the crew
    result = register_tool.run(
        tool_input={
            "crew_obj": tech_trends_crew,
            "name": "Tech Trends Analysis Crew",
            "port": 8080,
            "description": "A CrewAI agent that researches technology trends and writes reports",
            "api_token": api_key
        }
    )
    
    print(f"\nCrewAI agent registration result: {result}")
    print("You can now interact with your CrewAI agent using the address shown above.")
    print("The agent will respond to queries about technology trends.")
    print("\nTo test it, use a message with the QueryMessage model:")
    
    # Get the agent address from the result
    agent_info = register_tool.get_agent_info()
    if agent_info and "address" in agent_info:
        address = agent_info["address"]
        print("\nExample query using fetchai CLI:")
        print(f"fetchai message send --to {address} --payload '{{\"query\": \"What are the latest trends in AI?\"}}' --sign-with <your-key>")
    
    print("\nPress Ctrl+C to exit when done.")
    
    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main() 