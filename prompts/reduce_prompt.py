from langchain.prompts import PromptTemplate

def get_reduce_prompt(mode: str) -> PromptTemplate:
    if mode == "concise":
        return PromptTemplate.from_template("""다음은 chunk 단위 요약입니다. 전체 내용을 요약하되, **간결하게 정리**해주세요:

형식:
제목:
한 줄 요약:
핵심 내용 (2~4개):

--- 내용 ---
{text}

--- 요약 ---
제목:
...

한 줄 요약:
...

핵심 내용:
- 
- 
""")
    elif mode == "detailed":
        return PromptTemplate.from_template("""다음은 chunk 단위 요약입니다. 이들을 종합하여 **정리된 형태로 전체 요약**을 작성하세요.

형식:
제목:
한 줄 요약:
핵심 주제 목록 (3~5개):
상세 설명 (각 항목별):

--- 내용 ---
{text}

--- 요약 ---
제목:
...

한 줄 요약:
...

핵심 주제:
- 항목 1
- 항목 2
- 항목 3

상세 설명:
### 항목 1
...

### 항목 2
...

### 항목 3
...
""")
    else:
        raise ValueError("모드를 'concise' 또는 'detailed' 중 하나로 설정하세요.")
