from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
from chains.structured_summary_chain import get_structured_summary_chain
from loaders.md_loader import load_markdown
from splitters.token_splitter import split_documents

app = FastAPI()

class FilePathRequest(BaseModel):
    path: str

@app.post("/summarize")
def summarize_file(request: FilePathRequest):
    path = request.path

    if not os.path.exists(path):
        raise HTTPException(status_code=404, detail="파일이 존재하지 않습니다.")
    if not path.endswith(".md"):
        raise HTTPException(status_code=400, detail="지원되는 형식은 .md 파일입니다.")

    try:
        docs = load_markdown(path)
        split_docs = split_documents(docs)
        
        from chains.summarize_and_translate_chain import get_summary_and_translate_chain

        summarize_chain = get_summary_and_translate_chain(mode="detailed", lang="ko")
        raw_summary = summarize_chain.invoke(split_docs)

        structured_chain = get_structured_summary_chain()
        result = structured_chain.invoke([type("Doc", (), {"page_content": raw_summary})()])
        
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"요약 중 오류 발생: {str(e)}")
