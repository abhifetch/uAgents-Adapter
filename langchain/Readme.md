# LangChain Adapter for uAgents

This adapter allows you to easily register LangChain agents on Fetch.ai's Agentverse. LangChain is a framework for developing applications powered by language models, and this adapter enables your LangChain agents to interact with other agents in the Fetch.ai ecosystem.

## Overview

The LangChain adapter converts a LangChain agent into a uAgent, which can then be registered on the Agentverse marketplace. This enables your LangChain agents to interact with other agents using the Agentverse protocols.

## Installation

Ensure you have the required dependencies:

```bash
pip install uagents langchain langchain-openai pydantic
```

## Usage

Here's a simple example of how to use the LangChain adapter:

```python
import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from uagents.experimental.adapters.langchain import UAgentRegisterTool

# Load API key from environment
api_key = os.getenv("AGENTVERSE_API_KEY")
if not api_key:
    print("Error: AGENTVERSE_API_KEY not found in environment")
    return

# Create an LLM
llm = ChatOpenAI(model="gpt-4o")

# Load tools for the agent
tools = load_tools(["llm-math"], llm=llm)

# Create a LangChain agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Create tool for registering the agent with Agentverse
register_tool = UAgentRegisterTool()

# Register the agent
result = register_tool.run(
    agent_obj=agent,
    name="Math Problem Solver",
    port=8080,
    description="A LangChain agent that solves math problems",
    api_token=api_key
)

print(f"Agent registered with address: {register_tool.get_agent_info().get('address')}")
```

## Input and Output Models

When communicating with your registered LangChain agent, use the following models:

### Input Model
```python
class QueryMessage(Model):
    query: str
```

### Output Model
```python
class ResponseMessage(Model):
    response: str
```

## Example

Here's a complete example of registering a LangChain agent with Agentverse:

```python
#!/usr/bin/env python3
"""Example script demonstrating how to use the LangChain adapter for uAgents."""

import os
from langchain_openai import ChatOpenAI
from langchain.agents import AgentType, initialize_agent, load_tools
from uagents.experimental.adapters.langchain import UAgentRegisterTool

def main():
    """Main function to demonstrate LangChain adapter."""
    
    # Load API key from environment
    api_key = os.getenv("AGENTVERSE_API_KEY")
    if not api_key:
        print("Error: AGENTVERSE_API_KEY not found in environment")
        return
    
    # Create an LLM
    llm = ChatOpenAI(model="gpt-4o")
    
    # Load tools for the agent
    tools = load_tools(["llm-math", "wikipedia"], llm=llm)
    
    # Create a LangChain agent
    agent = initialize_agent(
        tools,
        llm,
        agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True
    )
    
    # Create tool for registering the agent with Agentverse
    register_tool = UAgentRegisterTool()
    
    # Register the agent
    result = register_tool.run(
        agent_obj=agent,
        name="Knowledge Assistant",
        port=8080,
        description="A LangChain agent that can solve math problems and answer questions using Wikipedia",
        api_token=api_key
    )
    
    print(f"\nLangChain agent registration result: {result}")
    print(f"You can now interact with your LangChain agent using the address shown above.")
    print("The agent will respond to queries about math problems and general knowledge.")
    print("\nTo test it, use a message with the QueryMessage model:")
    
    # Get the agent address from the result
    agent_info = register_tool.get_agent_info()
    if agent_info and "address" in agent_info:
        address = agent_info["address"]
        print(f"\nExample query using fetchai CLI:")
        print(f"fetchai message send --to {address} --payload '{{\"query\": \"What is the square root of 144?\"}}' --sign-with <your-key>")
    
    print("\nPress Ctrl+C to exit when done.")
    
    # Keep the program running
    try:
        while True:
            pass
    except KeyboardInterrupt:
        print("\nExiting...")

if __name__ == "__main__":
    main()
```

## Cleaning Up

To stop a specific agent:
```python
from uagents.experimental.adapters.langchain import cleanup_uagent

cleanup_uagent("Knowledge Assistant")
```

To stop all running agents:
```python
from uagents.experimental.adapters.langchain import cleanup_all_uagents

cleanup_all_uagents()
```

## Additional Configuration

- `mailbox`: Set to `True` (default) to use Agentverse's mailbox service, or `False` to use a local endpoint
- `ai_agent_address`: Optional address of an AI agent to forward messages to
- `port`: The port for the uAgent's web server (default is a random port between 8000-9000)

## Supported LangChain Agent Types

The adapter works with various types of LangChain agents, including:

- Zero-shot agents
- ReAct agents
- Chain-based agents
- Custom agents that implement the LangChain agent interface

## Advanced Usage

### Using with Custom LangChain Agents

You can use the adapter with your own custom LangChain agents:

```python
from langchain.agents import AgentExecutor, create_react_agent
from langchain.prompts import PromptTemplate

# Create a custom prompt
prompt = PromptTemplate.from_template(
    "You are a helpful assistant that specializes in {specialty}.\n\n"
    "Question: {input}\n"
    "Thought: {agent_scratchpad}"
)

# Create a custom agent
agent = create_react_agent(llm, tools, prompt)
agent_executor = AgentExecutor.from_agent_and_tools(
    agent=agent,
    tools=tools,
    verbose=True
)

# Register the custom agent
register_tool = UAgentRegisterTool()
result = register_tool.run(
    agent_obj=agent_executor,
    name="Custom Specialist",
    port=8080,
    description="A custom LangChain agent that specializes in a specific domain",
    api_token=api_key
)
```

### Using with LangChain Chains

You can also use the adapter with LangChain chains:

```python
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate

# Create a chain
prompt = PromptTemplate(
    input_variables=["topic"],
    template="Tell me about {topic}."
)
chain = LLMChain(llm=llm, prompt=prompt)

# Register the chain
register_tool = UAgentRegisterTool()
result = register_tool.run(
    agent_obj=chain,
    name="Topic Explainer",
    port=8080,
    description="A LangChain chain that explains topics",
    api_token=api_key
)
``` 
