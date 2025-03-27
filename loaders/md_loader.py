from langchain_community.document_loaders import TextLoader

def load_markdown(path: str):
    loader = TextLoader(path)
    return loader.load()
