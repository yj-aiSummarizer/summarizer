# 🧠 LangChain Markdown Summary App

This is a simple Streamlit app that uses LangChain and Groq LLMs (e.g., Mixtral) to summarize markdown-based conversation history.

## 📦 Features
- Upload `.md` files containing conversation history
- Automatically chunk and summarize using LangChain
- Map-Reduce style summarization
- Clean web interface with Streamlit
- Downloadable summary

## 🚀 Getting Started

### 1. Clone and Install

```bash
git clone https://github.com/your-username/llm_summary_project.git
cd llm_summary_project
pip install -r requirements.txt
```

### 2. Set up environment

Copy the sample and fill in your API key:
```bash
cp .env_sample .env
```

Edit `.env` and set:
```
GROQ_API_KEY=your_real_groq_api_key
```

### 3. Run the App

```bash
streamlit run streamlit_app.py
```

## 🛠 Project Structure

```
llm_summary_project/
├── chains/
├── config/
├── loaders/
├── prompts/
├── splitters/
├── streamlit_app.py
├── temp/
├── .env_sample
├── README.md
└── requirements.txt
```

## 📃 License
MIT


## 🔍 LangChain Tracing (Optional)

To enable LangChain Tracing via LangSmith, add these to your `.env`:

```
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=your_langsmith_api_key
LANGCHAIN_ENDPOINT=https://api.smith.langchain.com
```

Then go to https://smith.langchain.com to view traces of your app!
