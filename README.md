# Agent with Function Flow with Streamlit

A Streamlit-based AI research assistant that can answer questions using both a local document index and web search. The app combines a document ingestion pipeline, retrieval-augmented generation (RAG), and a function-driven agent workflow to help users research, summarize, and reason over uploaded files or live web results.

## Overview

This project is a Python application that lets you:

- Upload PDFs, TXT, or DOCX files
- Build a searchable vector index from the uploaded document
- Ask questions grounded in the indexed content
- Search the web for additional context using Tavily
- Run a multi-step function-based agent workflow with LLM orchestration
- View logs and intermediate steps during execution

It is designed as an interactive research desk, with the main interface in `main.py` and supporting modules for agent logic, file loading, RAG, and search tool integration.

## Features

- Streamlit web app interface
- Document indexing with ChromaDB / vector embeddings
- PDF, text, and DOCX support via loaders
- Search tools integration for web lookup
- LangChain and LangChain community toolchain support
- GPT-like model compatibility via Gemini, OpenAI, Mistral, Groq, Ollama, and others
- Configurable model and API key inputs from the sidebar
- Step-by-step execution logs for debugging and transparency

## Project Structure

```text
.
├── .streamlit/
│   └── config.toml
├── Agentic_Agent/
│   ├── __init__.py
│   ├── model.py
│   └── piplimimg.py
├── Tools/
│   ├── Rag/
│   │   ├── retrive.py
│   │   ├── system_setup.py
│   │   └── __init__.py
│   ├── search/
│   │   ├── search.py
│   │   └── __init__.py
│   └── __init__.py
├── fileLoder/
│   └── fileLoder.py
├── function_tool/
│   ├── evaluation.py
│   ├── final_result.py
│   ├── planner.py
│   ├── rage_response.py
│   ├── tool_function.py
│   ├── tool_run.py
│   └── updateQuery.py
├── .gitignore
├── ERRORS_AND_FIXES.md
├── main.py
├── requirements.txt
└── README.md
```

## Tech Stack

The project is built primarily in Python and uses:

- Streamlit
- LangChain
- LangChain Community
- LangChain Google GenAI
- LangChain Hugging Face
- ChromaDB / FAISS
- Google Generative AI
- OpenAI / Groq / Ollama / Mistral / OpenRouter support
- PDF and document parsing libraries (`pypdf`, `python-docx`)
- Tavily for web search
- Hugging Face embeddings

## Installation

1. Clone the repository:

```bash
git clone https://github.com/shahzaibkaramat67-coder/Agent_with_functions_flow_with_streamlit.git
cd Agent_with_functions_flow_with_streamlit
```

2. Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
# or
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

## Configuration

Create a `.env` file in the project root if you want to store your API keys outside the app UI.

Example:

```env
GEMINI_NEW_API_KEY=your_gemini_api_key
TAVILY_API_KEY=your_tavily_api_key
GEMINI_API_MODEL=gemini-2.5-flash
EMBADDING_MODEL_SENTENCE=sentence-transformers/all-MiniLM-L6-v2
```

You can also enter these keys directly in the sidebar of the Streamlit app.

## Running the App

Start the app with:

```bash
streamlit run main.py
```

Then open the local URL shown in the terminal in your browser.

## Usage

1. Open the app in the browser.
2. In the sidebar, configure the model and API keys.
3. Upload a document (PDF, TXT, or DOCX).
4. Click "Build document index".
5. Ask a question in the chat input.
6. The agent will use the indexed document and/or web search to generate an answer.

## Notes

- Document indexing is performed in the session using the uploaded file and vector database setup.
- The app supports both local knowledge grounding and external search.
- Some models and integrations require additional API keys and internet access.

## License

This project does not appear to include a license file in the repository. If you plan to publish or distribute it, add an appropriate open-source license before sharing it publicly.

## Repository Context

This repository is a research-oriented AI assistant prototype and can be extended for:

- custom RAG workflows
- multi-tool agent planning
- document analysis pipelines
- searchable knowledge assistants
- team research copilots

