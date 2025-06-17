# # pip install langchain-openai python-dotenv

"""# Basic OpenAI setup:

from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

# Initialize the OpenAI client
client = OpenAI(api_key=openai_api_key)

# Make a Chat Completion request
response = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is the capital of India?"}
    ],
    temperature=0.3
)

# Print the assistant's reply
print(response.choices[0].message.content)
"""

# Langchain OpenAI setup

from langchain_openai import ChatOpenAI 
from dotenv import load_dotenv
import os

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0.3,
    api_key=openai_api_key
)

response = llm.invoke("What is the capital of India?")
print(response.content)

