"""Example of using UAgentRegisterTool with a Tavily search agent."""

import os
import time
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.agents import initialize_agent, AgentType, Tool
from langchain_community.tools.tavily_search import TavilySearchResults
from uagents.experimental.adapters.langchain import UAgentRegisterTool,cleanup_uagent

# Load environment variables
load_dotenv()

# Set your API keys - for production, use environment variables instead of hardcoding
os.environ["OPENAI_API_KEY"] = "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"
os.environ["TAVILY_API_KEY"] = "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"

# Get API token for Agentverse
API_TOKEN = os.environ["AV_API_KEY"] = "eyJhbGciOiJSUzI1NiJ9.eyJleHAiOjE3NDYwMTQxNDIsImdycCI6ImludGVybmFsIiwiaWF0IjoxNzQzNDIyMTQyLCJpc3MiOiJmZXRjaC5haSIsImp0aSI6IjllNmI1OWQ4YjM4YzBkZjliNWVhNTg1MyIsInNjb3BlIjoiYXYiLCJzdWIiOiIyMGI0MGZiN2IxNDZiNzRlYzU4ZGRkZGU4YzMwZjQwZmE3NDhjMmMyNDZlMjY1OTQifQ.d2OY57N_0lflER5mDMgqpYFHsuuwPNunZMMhnaI-Afyvl2jo5otUcwH53y9UnNNzFbfdRRJ_ja_3FUpCEN1_HLFR45UVBWYAlIHsajB1Ex8HfhLmNPSov50Db4NqeP5EUyoh9MFVBQIGSXLkDD2J2_yIEytpnszdRN6AQNsf2yu2wqabLlHbs5gbAuB2_KcqN5c_uM0JiuYobUUu-1bRInamXGKNwpVsX0qS4mUkzRd6BbcyRMUQEbLb9hiNJG5DpgROB3JTEL1ORNtq_Xvj8O-VC9j9KyQwEOkpllLjzRkmDw3jtANLiNRMqK_FhZROx5-S9G_kSyevOzgISE7_zw"

if not API_TOKEN:
    raise ValueError("Please set AV_API_KEY environment variable")

# Define the tools the agent will use
tools = [
    TavilySearchResults(
        max_results=3,
        description="Useful for searching the web for current information and getting relevant results"
    )
]

# Create the LLM
llm = ChatOpenAI(temperature=0)

# Create the agent using initialize_agent (like in calculator_agent.py)
agent = initialize_agent(
    tools=tools,
    llm=llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Create and register the uAgent
tool = UAgentRegisterTool()
agent_info = tool.invoke({
    "agent_obj": agent,
    "name": "tavily_search_agent",
    "port": 8080,
    "description": "A search agent for finding information on the web using Langchain and Tavily",
    "api_token": API_TOKEN,
    "ai_agent_address": "agent1qtlpfshtlcxekgrfcpmv7m9zpajuwu7d5jfyachvpa4u3dkt6k0uwwp2lct"
})

# Print agent info
print(f"Created uAgent '{agent_info['name']}' with address {agent_info['address']} on port {agent_info['port']}")

# Keep the agent running
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    print("\nShutting down search agent...")
    cleanup_uagent("tavily_search_agent")  # Make sure the name matches what was used above
    print("Search agent stopped.")
