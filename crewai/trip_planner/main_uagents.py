#!/usr/bin/env python3
"""Trip Planner script using CrewAI adapter for uAgents."""

import os
from crewai import Crew
from textwrap import dedent
from trip_agents import TripAgents
from trip_tasks import TripTasks
from uagents.experimental.adapters.crewai import CrewAIRegisterTool
from dotenv import load_dotenv

def main():
    """Main function to demonstrate Trip Planner with CrewAI adapter."""
    
    # Load API key from environment
    load_dotenv()
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("Error: AGENTVERSE_API_KEY not found in environment")
        return
    
    # Get user inputs
    print("## Welcome to Trip Planner Crew")
    print('-------------------------------')
    origin = input(
        dedent("""
            From where will you be traveling from?
        """))
    cities = input(
        dedent("""
            What are the cities options you are interested in visiting?
        """))
    date_range = input(
        dedent("""
            What is the date range you are interested in traveling?
        """))
    interests = input(
        dedent("""
            What are some of your high level interests and hobbies?
        """))
    
    # Create agents and tasks
    agents = TripAgents()
    tasks = TripTasks()

    city_selector_agent = agents.city_selection_agent()
    local_expert_agent = agents.local_expert()
    travel_concierge_agent = agents.travel_concierge()

    identify_task = tasks.identify_task(
        city_selector_agent,
        origin,
        cities,
        interests,
        date_range
    )
    gather_task = tasks.gather_task(
        local_expert_agent,
        origin,
        interests,
        date_range
    )
    plan_task = tasks.plan_task(
        travel_concierge_agent, 
        origin,
        interests,
        date_range
    )
    
    # Create crew
    trip_planner_crew = Crew(
        agents=[
            city_selector_agent, local_expert_agent, travel_concierge_agent
        ],
        tasks=[identify_task, gather_task, plan_task],
        verbose=True
    )
    
    # Create tool for registering the crew with Agentverse
    register_tool = CrewAIRegisterTool()
    
    # Register the crew
    result = register_tool.run(
        tool_input={
            "crew_obj": trip_planner_crew,
            "name": "Trip Planner Crew",
            "port": 8080,
            "description": "A CrewAI agent that helps plan trips based on preferences",
            "api_token": api_key,
            "mailbox" : True
        }
    )
    
    print(f"\nCrewAI agent registration result: {result}")
    print(f"You can now interact with your CrewAI agent using the address shown above.")
    print("The agent will respond to queries about trip planning.")
    print("\nTo test it, use a message with the QueryMessage model:")
    
    # Get the agent address from the result
    agent_info = register_tool.get_agent_info()
    if agent_info and "address" in agent_info:
        address = agent_info["address"]
        print(f"\nExample query using fetchai CLI:")
        print(f"fetchai message send --to {address} --payload '{{\"query\": \"What are the best cities for my interests?\"}}' --sign-with <your-key>")
    
    print("\nPress Ctrl+C to exit when done.")
    
    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()

