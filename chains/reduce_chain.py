from langchain_core.output_parsers import StrOutputParser
from config.settings import llm
from prompts.reduce_prompt import reduce_prompt

reduce_chain = reduce_prompt | llm | StrOutputParser()
