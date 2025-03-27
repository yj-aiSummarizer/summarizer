from langchain_core.output_parsers import StrOutputParser
from config.settings import llm
from prompts.map_prompt import map_prompt

map_chain = map_prompt | llm | StrOutputParser()
