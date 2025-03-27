from langchain.prompts import PromptTemplate

def get_map_prompt(mode: str) -> PromptTemplate:
    if mode == "concise":
        return PromptTemplate.from_template("""당신은 전문 요약가입니다. 아래 텍스트는 전체 대화의 일부입니다.
주요 내용을 **간결하게 bullet 2~3개로 요약**하세요.

--- 내용 ---
{text}

--- 요약 ---
- 
- 
""")
    elif mode == "detailed":
        return PromptTemplate.from_template("""당신은 전문 요약가입니다. 다음은 전체 대화 중 일부입니다.

이 chunk에서 중요한 사실, 질문, 응답을 **구체적이고 설명적으로** 요약하세요.
- bullet은 최대 3개
- 정보는 자세히, 단 문장은 짧게

--- 내용 ---
{text}

--- 요약 ---
- 
- 
- 
""")
    else:
        raise ValueError("모드를 'concise' 또는 'detailed' 중 하나로 설정하세요.")
