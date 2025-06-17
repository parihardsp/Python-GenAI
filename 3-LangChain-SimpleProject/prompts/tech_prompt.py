from langchain.prompts import PromptTemplate

tech_prompt = PromptTemplate(
    input_variables=["country"],
    template="What are the top 2 emerging tech trends in {country} for 2024? Briefly explain each."
)
