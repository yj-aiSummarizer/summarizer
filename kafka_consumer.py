import json
import os
import threading
from kafka import KafkaConsumer, KafkaProducer
from loaders.md_loader import load_markdown
from splitters.token_splitter import split_documents
from chains.summarize_and_translate_chain import get_summary_and_translate_chain
from formatters.summary_formatter import FormatterFactory

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
            print(f"✅ 요약 완료: {path}")
        except Exception as e:
            print(f"❌ 오류 처리 중: {path}, 예외: {str(e)}")

if __name__ == "__main__":
    print("📡 Kafka Consumer 시작됨...")
    threading.Thread(target=run_kafka_consumer, daemon=False).start()
