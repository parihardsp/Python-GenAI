from langchain.prompts import PromptTemplate

prompt_template = """
List the top 2 books on the topic: {topic}, along with a 1-line summary of each.
"""

book_prompt = PromptTemplate(
    input_variables=["topic"],
    template=prompt_template.strip()
)
