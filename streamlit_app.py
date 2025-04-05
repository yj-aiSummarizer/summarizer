import streamlit as st
import os
import json
import requests
import subprocess
from kafka import KafkaConsumer, KafkaProducer
import threading
import time

from loaders.md_loader import load_markdown
from splitters.token_splitter import split_documents
from chains.structured_summary_chain import get_structured_summary_chain
from chains.summarize_and_translate_chain import get_summary_and_translate_chain
from formatters.summary_formatter import FormatterFactory


def process_uploaded_file(uploaded_file, mode_key, lang_key, formatter):
    os.makedirs("temp", exist_ok=True)
    file_path = os.path.join("temp", uploaded_file.name)

    with open(file_path, "wb") as f:
        f.write(uploaded_file.read())

    docs = load_markdown(file_path)
    split_docs = split_documents(docs)

    if formatter.get_extension() == "json":
        # from chains.summarize_and_translate_chain import get_summary_and_translate_chain

        summarize_chain = get_summary_and_translate_chain(mode="detailed", lang="ko")
        raw_summary = summarize_chain.invoke(split_docs)

        structured_chain = get_structured_summary_chain()
        result = structured_chain.invoke([type("Doc", (), {"page_content": raw_summary})()])
        formatted = formatter.format(result)
    else:
        chain = get_summary_and_translate_chain(mode_key, lang_key)
        raw_result = chain.invoke(split_docs)
        formatted = formatter.format(raw_result)

    if not isinstance(formatted, str):
        try:
            formatted = json.dumps(formatted, ensure_ascii=False, indent=2)
        except Exception:
            formatted = str(formatted)

    ext = formatter.get_extension()
    return formatted, ext


def display_result(formatted, ext):
    st.success("✅ 요약 완료!")
    st.subheader("📌 요약 결과")
    st.markdown(formatted, unsafe_allow_html=True)

    st.download_button(
        label=f"📥 요약 결과 다운로드 (.{ext})",
        data=formatted.encode("utf-8"),
        file_name=f"summary.{ext}",
        mime="text/plain"
    )


def main():
    st.set_page_config(page_title="Markdown AI 요약기", layout="wide")
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(["🧠 요약기 사용하기", "🔗 API 테스트", "🧪 IntelliJ 테스트", "📡 Kafka 통신 테스트", "📤 Kafka 요청 전송", "🛰 Kafka Consumer 실행"])

    with tab1:
        st.title("🧠 Markdown 요약기 - Streamlit 앱")

        uploaded_file = st.file_uploader("📄 요약할 .md 파일을 업로드하세요", type=["md"])

        mode = st.selectbox("요약 모드 선택", ["간결 요약", "상세 요약"])
        mode_key = "concise" if mode == "간결 요약" else "detailed"

        lang_display = st.selectbox("출력 언어 선택", ["한국어", "영어"])
        lang_key = "en" if lang_display == "영어" else "ko"

        output_format = st.selectbox("출력 포맷 선택", ["markdown", "json", "html", "text"])
        formatter = FormatterFactory.get_formatter(output_format)

        if uploaded_file:
            st.success("📂 파일 업로드 완료")
            if st.button("🧠 요약하기"):
                with st.spinner("문서 처리 중..."):
                    formatted, ext = process_uploaded_file(uploaded_file, mode_key, lang_key, formatter)
                display_result(formatted, ext)
        else:
            st.info("왼쪽에 .md 파일을 업로드하고, 요약 모드/언어/포맷을 선택하세요.")

    with tab2:
        st.title("🔗 API 테스트")

        st.write("📂 요약할 Markdown 파일 경로를 직접 입력하거나 Finder에서 선택할 수 있습니다.")
        uploaded_api_file = st.file_uploader("🔍 Finder에서 파일 선택 (선택사항)", type=["md"], key="api_file")

        file_path = st.text_input("또는 직접 경로 입력", value="", key="manual_path")

        final_path = ""
        if uploaded_api_file:
            temp_api_path = os.path.join("temp", uploaded_api_file.name)
            os.makedirs("temp", exist_ok=True)
            with open(temp_api_path, "wb") as f:
                f.write(uploaded_api_file.read())
            final_path = temp_api_path
            st.info(f"📁 선택된 파일 경로: {final_path}")
        else:
            final_path = file_path

        if "api_result" not in st.session_state:
            st.session_state["api_result"] = None

        if st.button("🚀 API 호출"):
            if final_path:
                with st.spinner("API 요청 중..."):
                    try:
                        response = requests.post("http://localhost:8000/summarize", json={"path": final_path})
                        if response.status_code == 200:
                            st.session_state["api_result"] = response.json()
                            st.success("✅ 요약 완료!")
                        else:
                            st.error(f"❌ 오류 발생: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"❌ 예외 발생: {str(e)}")
            else:
                st.warning("파일 경로를 입력하거나 파일을 선택해주세요.")

        if st.session_state["api_result"]:
            beautify_json = st.checkbox("🧩 JSON 보기 형식: Beautify", value=True)
            if beautify_json:
                st.json(st.session_state["api_result"])
            else:
                st.code(json.dumps(st.session_state["api_result"], indent=2, ensure_ascii=False), language="json")

    with tab3:
        st.title("🧪 IntelliJ 테스트")

        st.write("📂 Spring 서버에서 사용할 Markdown 파일을 선택하거나 경로를 직접 입력하세요.")
        uploaded_spring_file = st.file_uploader("🔍 Finder에서 파일 선택 (선택사항)", type=["md"], key="spring_file")

        spring_file_path = st.text_input("또는 직접 경로 입력", value="", key="spring_path")

        final_spring_path = ""
        if uploaded_spring_file:
            temp_spring_path = os.path.join("temp", uploaded_spring_file.name)
            os.makedirs("temp", exist_ok=True)
            with open(temp_spring_path, "wb") as f:
                f.write(uploaded_spring_file.read())
            final_spring_path = temp_spring_path
            st.info(f"📁 선택된 파일 경로: {final_spring_path}")
        else:
            final_spring_path = spring_file_path

        if st.button("🚀 Spring API 호출"):
            if final_spring_path:
                with st.spinner("Spring 서버에 요청 중..."):
                    try:
                        response = requests.get("http://localhost:8080/api/summary", params={"filePath": final_spring_path})
                        if response.status_code == 200:
                            spring_result = response.json()
                            st.success("✅ Spring 서버 요약 완료!")
                            st.json(spring_result)
                        else:
                            st.error(f"❌ 오류 발생: {response.status_code}  - {response.text}")
                    except Exception as e:
                        st.error(f"❌ 예외 발생: {str(e)}")
            else:
                st.warning("파일 경로를 입력해주세요.")

    with tab4:
        st.title("📡 Kafka 통신 테스트")

        kafka_status = st.empty()
        kafka_result_box = st.empty()

        if "kafka_result" not in st.session_state:
            st.session_state["kafka_result"] = []

        def run_kafka_consumer():
            consumer = KafkaConsumer(
                'md-file-requests',
                bootstrap_servers='localhost:9092',
                group_id='summarizer-group',
                auto_offset_reset='earliest',
                value_deserializer=lambda m: m.decode('utf-8')
            )

            producer = KafkaProducer(
                bootstrap_servers='localhost:9092',
                value_serializer=lambda m: m.encode('utf-8')
            )

            for msg in consumer:
                path = msg.value
                kafka_status.info(f"📥 수신된 파일 경로: {path}")
                try:
                    docs = load_markdown(path)
                    split_docs = split_documents(docs)
                    chain = get_summary_and_translate_chain(mode="detailed", lang="ko")
                    result = chain.invoke(split_docs)
                    formatted_result = FormatterFactory.get_formatter("markdown").format(result)

                    if not isinstance(formatted_result, str):
                        try:
                            formatted_result = json.dumps(formatted_result, ensure_ascii=False, indent=2)
                        except Exception:
                            formatted_result = str(formatted_result)

                    producer.send('md-file-responses', formatted_result)
                    st.session_state["kafka_result"].append(f"요약 완료 및 전송: {formatted_result[:100]}...")
                except Exception as e:
                    st.session_state["kafka_result"].append(f"❌ 오류: {str(e)}")
                kafka_result_box.markdown("\n\n".join(st.session_state["kafka_result"][-5:]))

        if st.button("▶️ Kafka Consumer 시작"):
            kafka_status.info("Kafka Consumer를 시작합니다...")
            threading.Thread(target=run_kafka_consumer, daemon=True).start()

    with tab5:
        st.title("📤 Kafka 요청 전송 (Spring API 호출)")

        uploaded_kafka_file = st.file_uploader("🔍 Finder에서 파일 선택 (선택사항)", type=["md"], key="kafka_request_file")
        manual_kafka_path = st.text_input("또는 직접 경로 입력", value="", key="manual_kafka_path")

        final_kafka_path = ""
        if uploaded_kafka_file:
            temp_kafka_path = os.path.join("temp", uploaded_kafka_file.name)
            os.makedirs("temp", exist_ok=True)
            with open(temp_kafka_path, "wb") as f:
                f.write(uploaded_kafka_file.read())
            final_kafka_path = temp_kafka_path
            st.info(f"📁 선택된 파일 경로: {final_kafka_path}")
        else:
            final_kafka_path = manual_kafka_path

        if st.button("🚀 Kafka 전송 요청 (Spring API 호출)"):
            if final_kafka_path:
                with st.spinner("Spring Kafka API 호출 중..."):
                    try:
                        response = requests.post(
                            "http://localhost:8080/api/kafka/send-path",
                            json={"path": final_kafka_path}
                        )
                        if response.status_code == 200:
                            st.success(f"✅ Kafka 요청 성공: {response.text}")
                        else:
                            st.error(f"❌ 오류 발생: {response.status_code} - {response.text}")
                    except Exception as e:
                        st.error(f"❌ 예외 발생: {str(e)}")

    with tab6:
        st.title("🛰 Kafka Consumer 실행")
        st.write("외부 kafka_consumer.py 파일을 실행합니다.")

        if st.button("▶️ Kafka Consumer 실행 (백그라운드)"):
            try:
                subprocess.Popen(["python", "kafka_consumer.py"])
                st.success("✅ kafka_consumer.py 실행 시작됨 (백그라운드)")
            except Exception as e:
                st.error(f"❌ 실행 실패: {str(e)}")


if __name__ == "__main__":
    main()
