from langchain_openai import ChatOpenAI 

from dotenv import load_dotenv

load_dotenv()

def get_llm():
    return ChatOpenAI(
        model_name="gpt-3.5-turbo",
        temperature=0.7)
