from langchain.agents import initialize_agent, AgentType
from langchain_openai import ChatOpenAI
from tools.news_tool import get_wikipedia_summary, get_latest_news
from dotenv import load_dotenv
import os

load_dotenv()

llm = ChatOpenAI(temperature=0, model="gpt-4")

# List of tools the agent can call
tools = [get_latest_news, get_wikipedia_summary]

# Build an agent that can reason and decide
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True
)

# Ask it a question
question = "Tell me about recent news and background info on Tesla"
response = agent.invoke(question)

print("\n✅ Final Answer:")
print(response)
