from langchain_core.runnables import RunnableLambda
from pydantic import BaseModel, Field
from config.settings import llm


# 1. 요약 결과를 위한 Pydantic 스키마 정의
class SummarySchema(BaseModel):
    title: str = Field(description="요약의 제목")
    summary: str = Field(description="한 줄 요약")
    bullets: list[str] = Field(description="번호 없이 문자열로만 구성된 bullet 포인트 리스트 (예: '내용 요약')")


def clean_bullets(bullets: list[str]) -> list[str]:
    return [b.split(":", 1)[-1].strip() if ":" in b else b for b in bullets]


# 2. 체인 생성 함수
def get_structured_summary_chain():
    def summarize(docs):
        result = llm.with_structured_output(SummarySchema).invoke(
            "\n\n".join([doc.page_content for doc in docs])
        )

        if isinstance(result, BaseModel):
            result = result.dict()

        cleaned_bullets = [b.split(":", 1)[-1].strip() if ":" in b else b for b in result.get("bullets", [])]
        result["bullets"] = cleaned_bullets

        return result

    return RunnableLambda(summarize)