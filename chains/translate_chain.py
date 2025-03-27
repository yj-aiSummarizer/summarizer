from langchain.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from config.settings import llm
from langchain_core.runnables import RunnableLambda

def get_translation_chain(target_lang: str):
    if target_lang == "ko":
        prompt = PromptTemplate.from_template("""다음 영어 텍스트를 자연스럽고 전문적으로 **한국어로 번역**해주세요.

--- 영어 원문 ---
{text}

--- 한국어 번역 ---
""")
    elif target_lang == "en":
        prompt = PromptTemplate.from_template("""Please translate the following text to **natural English**.

--- 원문 ---
{text}

--- English translation ---
""")
    else:
        raise ValueError("지원하지 않는 언어입니다.")

    return prompt | llm | StrOutputParser()

translate_node_ko = RunnableLambda(lambda text: get_translation_chain("ko").invoke({"text": text}))
