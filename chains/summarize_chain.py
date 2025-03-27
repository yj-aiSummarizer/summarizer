from langchain_core.output_parsers import StrOutputParser
from config.settings import llm
from prompts.map_prompt import get_map_prompt
from prompts.reduce_prompt import get_reduce_prompt
from langchain_core.runnables import RunnableLambda

def get_summary_chain(mode: str = "detailed"):
    map_prompt = get_map_prompt(mode)
    reduce_prompt = get_reduce_prompt(mode)

    map_chain = map_prompt | llm | StrOutputParser()
    reduce_chain = reduce_prompt | llm | StrOutputParser()

    def map_reduce_chain(docs):
        summaries = [map_chain.invoke({"text": doc.page_content}) for doc in docs]
        combined_input = {"text": "\n\n".join(summaries)}
        return reduce_chain.invoke(combined_input)

    return RunnableLambda(map_reduce_chain)
