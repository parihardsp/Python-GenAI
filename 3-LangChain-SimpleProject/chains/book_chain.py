from prompts.book_prompt import book_prompt
from utils.llm_provider import get_llm

llm = get_llm()
book_chain = book_prompt | llm
