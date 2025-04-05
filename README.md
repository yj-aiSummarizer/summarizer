# 🧠 LLM Markdown Summarizer

LangChain 기반 LLM을 활용해 Markdown 문서를 요약하고, 다양한 포맷으로 출력할 수 있는 웹 애플리케이션입니다.

---

## 🔧 주요 기능

- 📂 `.md` 파일 업로드
- 🧠 대화형 요약: 간결 / 상세 모드 선택
- 🌐 출력 언어 선택: 한국어 / 영어
- 📄 요약 포맷 선택: Markdown / JSON / HTML / 텍스트
- 💬 요약 후 영어 → 한국어 자동 번역 (옵션)
- ⬇️ 결과 다운로드 (.md / .json / .html / .txt)

---

## 🏗️ 기술 스택

- [LangChain](https://www.langchain.com/)
- [Streamlit](https://streamlit.io/)
- Python 3.9+
- Groq (LLM API)
- LangSmith (옵션)

---

## 📁 프로젝트 구조

```
llm_summary_project/
├── streamlit_app.py               # Streamlit 기반 웹 인터페이스
├── chains/
│   ├── summarize_chain.py         # 요약 체인 (MapReduce)
│   ├── translate_chain.py         # 번역 체인 (en → ko)
│   └── summarize_and_translate_chain.py
├── formatters/
│   └── summary_formatter.py       # Markdown/JSON/HTML/Text Formatter 추상화
├── prompts/
│   ├── map_prompt.py              # 요약 (chunk별)
│   └── reduce_prompt.py           # 요약 (통합)
├── loaders/
│   └── md_loader.py               # Markdown 문서 로더
├── splitters/
│   └── token_splitter.py          # 문서 chunk 분할
├── config/
│   └── settings.py                # Groq 및 LangChain 설정
├── .env_sample                    # 환경변수 예시
├── requirements.txt               # 의존성 목록
└── README.md
```

---

## ⚙️ 실행 방법

```bash
# 1. 의존성 설치
pip install -r requirements.txt

# 2. 환경변수 설정
cp .env_sample .env
# .env 파일에 GROQ_API_KEY=... 입력l

# 3. 실행
streamlit run streamlit_app.py
```

---

## 📝 .env_sample 예시

```
GROQ_API_KEY=your_groq_api_key_here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key  # 선택 사항
```

---

## 🧪 향후 확장 아이디어

- [ ] FastAPI 기반 REST API 버전
- [ ] Docker 배포 구성
- [ ] DB 저장 및 목록 조회 기능
- [ ] 키워드 추출, 유사 문서 추천 등 추가 분석 기능

---

## 📄 License

MIT License
