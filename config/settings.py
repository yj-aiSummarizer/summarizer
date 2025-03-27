import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

# .env 파일 로드
load_dotenv()

# 환경 변수에서 API 키 불러오기
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

if not GROQ_API_KEY:
    raise ValueError("GROQ_API_KEY가 설정되어 있지 않습니다. .env 파일을 확인하세요.")

# Groq LLM 설정
llm = ChatGroq(
    model="llama3-8b-8192",
    temperature=0.2,
    api_key=GROQ_API_KEY  # ✅ 여기에 전달
)

CHUNK_SIZE = 1024
CHUNK_OVERLAP = 100
