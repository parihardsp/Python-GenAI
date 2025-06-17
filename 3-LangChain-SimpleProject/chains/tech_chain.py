# from langchain.chains import LLMChain
# from prompts.tech_prompt import tech_prompt
# from utils.llm_provider import get_llm

# llm = get_llm()
# tech_chain = LLMChain(llm=llm, prompt=tech_prompt)

from prompts.tech_prompt import tech_prompt
from utils.llm_provider import get_llm

llm = get_llm()
tech_chain = tech_prompt | llm
