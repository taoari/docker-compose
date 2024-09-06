import phoenix as px
from phoenix.trace.langchain import LangChainInstrumentor

# # To view traces in Phoenix, you will first have to start a Phoenix server. You can do this by running the following:
# session = px.launch_app()

# Initialize Langchain auto-instrumentation
LangChainInstrumentor().instrument()

# langchain_calc_agent.py

from langchain import OpenAI
from langchain.tools import Tool
from langchain.agents import initialize_agent, AgentType

# Define the calculator tool
def calculator(expression: str) -> str:
    try:
        return str(eval(expression))
    except Exception as e:
        return str(e)

calc_tool = Tool(
    name="Calculator",
    func=calculator,
    description="This tool evaluates basic mathematical expressions, e.g., '2 + 2'.",
)

# Initialize the LLM
llm = OpenAI(temperature=0)

# List of tools (only calculator tool)
tools = [calc_tool]

# Initialize the agent
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
)

# Test the agent
if __name__ == "__main__":
    query = "What is 10 + 15?"
    response = agent.run(query)
    print(response)
