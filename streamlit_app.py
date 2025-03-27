import streamlit as st
import os
import json

from loaders.md_loader import load_markdown
from splitters.token_splitter import split_documents
from chains.summarize_and_translate_chain import get_summary_and_translate_chain
from formatters.summary_formatter import FormatterFactory

st.set_page_config(page_title="Markdown AI 요약기", layout="wide")
st.title("🧠 AI 기반 Markdown 요약기")

uploaded_file = st.file_uploader("📄 요약할 .md 파일을 업로드하세요", type=["md"])

mode = st.selectbox("요약 모드 선택", ["간결 요약", "상세 요약"])
mode_key = "concise" if mode == "간결 요약" else "detailed"

lang_display = st.selectbox("출력 언어 선택", ["한국어", "영어"])
lang_key = "en" if lang_display == "영어" else "ko"

output_format = st.selectbox("출력 포맷 선택", ["markdown", "json", "html", "text"])
formatter = FormatterFactory.get_formatter(output_format)

if uploaded_file:
    with st.spinner("문서 처리 중..."):
        os.makedirs("temp", exist_ok=True)
        file_path = os.path.join("temp", uploaded_file.name)

        with open(file_path, "wb") as f:
            f.write(uploaded_file.read())

        docs = load_markdown(file_path)
        split_docs = split_documents(docs)

        # 요약 + 번역 실행
        chain = get_summary_and_translate_chain(mode_key, lang_key)
        raw_summary = chain.invoke(split_docs)

        # ✅ 포맷터 적용 후 str 보장
        formatted = formatter.format(raw_summary)
        if not isinstance(formatted, str):
            try:
                formatted = json.dumps(formatted, ensure_ascii=False, indent=2)
            except Exception:
                formatted = str(formatted)

        ext = formatter.get_extension()

    st.success("✅ 요약 완료!")
    st.subheader("📌 요약 결과")
    st.markdown(formatted, unsafe_allow_html=True)

    st.download_button(
        label=f"📥 요약 결과 다운로드 (.{ext})",
        data=formatted.encode("utf-8"),
        file_name=f"summary.{ext}",
        mime="text/plain"
    )
else:
    st.info("왼쪽에 .md 파일을 업로드하고, 요약 모드/언어/포맷을 선택하세요.")
