from langchain_text_splitters import TokenTextSplitter
from config.settings import CHUNK_SIZE, CHUNK_OVERLAP

def split_documents(docs):
    splitter = TokenTextSplitter(chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP)
    return splitter.split_documents(docs)
