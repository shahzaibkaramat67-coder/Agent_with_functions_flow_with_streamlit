# Agent with Function Flow with Streamlit

A Streamlit AI research assistant that combines document-based RAG, web search, and a function-driven planning loop to answer user questions with context-aware reasoning.

This project is designed as an interactive "research desk" where a user can upload a document, build a searchable vector index, and ask questions that may be answered from either the uploaded content or the live web. The app uses an agent workflow to decide whether a question should be answered from a local document store, a search engine, or a combination of both.

## Overview

The app works in three layers:

1. User interface: a Streamlit app for uploading documents, setting API keys, and interacting with the assistant.
2. Agent orchestration: a multi-step loop that rewrites the question, selects a tool, evaluates whether the result is sufficient, and plans the next action.
3. Retrieval and generation: a local RAG pipeline backed by ChromaDB plus web search support through Tavily.

The code is organized around a single main app entry point plus modular components for the LLM, tool selection, evaluation, planning, and retrieval.

## Key Features

- Streamlit-based chat interface
- Upload PDF, TXT, and DOCX documents
- Build a local vector index from uploaded documents
- Search the web with Tavily
- Use a retrieval-augmented generation flow over the indexed document
- Run an iterative agent loop with tool selection, evaluation, and replanning
- Display intermediate step logs for transparency and debugging
- Configure Gemini model and API settings from the app sidebar

## Architecture

### 1. Streamlit Frontend

`main.py` is the main application entry point. It handles:

- app configuration via `st.set_page_config()`
- sidebar configuration for API keys and model names
- document upload and indexing
- chat-based interaction with the assistant
- execution logs and step-by-step outputs

The app stores session state for:

- chat history
- indexing status
- logs
- conversation steps

### 2. Agent Core

`Agentic_Agent/piplimimg.py` contains the main entry function:

- `entryPoint(user_input, log_callback=None)`
- Rewrites the user query
- Selects the next tool using an LLM-based tool selector
- Runs the tool
- Evaluates whether enough information exists
- Uses a planner to decide whether to continue with another search or RAG request
- Returns a final answer along with steps and status

This makes the project a function-calling style agent rather than a simple single-pass chatbot.

### 3. Tool Selection and Planning

The `function_tool/` package contains the logic for selecting tools and deciding the next move:

- `tool_function.py`: chooses between `SEARCH`, `RAG`, and `NONE` based on the user query
- `tool_run.py`: executes the selected tool
- `evaluation.py`: checks whether the retrieved data is sufficient to answer the query
- `planner.py`: decides whether the agent should continue searching or finish
- `final_result.py`: formats the final answer using the LLM
- `updateQuery.py`: rewrites or rephrases the input to improve tool usage

### 4. Document Loader

`fileLoder/fileLoder.py` supports multiple document types:

- `.pdf` via `PyPDFLoader`
- `.txt` via `TextLoader`
- `.docx` via `Docx2txtLoader`
- URLs via `WebBaseLoader`

This gives the project flexibility for both local document ingestion and remote content loading.

### 5. RAG Pipeline

`Tools/Rag/system_setup.py` creates the Chroma vector store:

- splits documents using `RecursiveCharacterTextSplitter`
- embeds chunks using `HuggingFaceEmbeddings`
- persists the database under `data/chroma_db`

`Tools/Rag/retrive.py`:

- loads the vector database
- retrieves the most relevant documents using MMR search
- optionally reranks results
- constructs a prompt for the LLM
- returns a grounded answer based strictly on the document context

### 6. Web Search

`Tools/search/search.py` calls the Tavily API to retrieve search results:

- the query is sent to Tavily
- result title, snippet content, and URL are formatted into a context string
- that content is then passed back to the agent for evaluation and answer generation

### 7. LLM Setup

`Agentic_Agent/model.py` configures the model layer:

- reads the Gemini API key from environment variables or the app session
- reads the model name from `GEMINI_API_MODEL` or `GEMINI_API_MODEL_LITE`
- uses `GoogleGenerativeAI` to create the LLM client

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
│   │   ├── __init__.py
│   │   ├── retrive.py
│   │   └── system_setup.py
│   ├── search/
│   │   ├── __init__.py
│   │   └── search.py
│   └── __init__.py
├── fileLoder/
│   ├── __pycache__/
│   └── fileLoder.py
├── function_tool/
│   ├── __pycache__/
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
├── README.md
└── uploads/
```

## Dependencies

The project uses a large Python stack, including:

- streamlit
- python-dotenv
- langchain
- langchain-core
- langchain-community
- langchain-google-genai
- langchain-huggingface
- langchain-text-splitters
- google-generativeai
- google-genai
- openai
- groq
- mistralai
- openrouter
- chromadb
- faiss-cpu
- pypdf
- beautifulsoup4
- requests
- tiktoken
- tavily-python
- pydantic
- huggingface_hub
- sentence-transformers
- duckduckgo-search
- ddgs
- ollama
- langchain_ollama
- python-docx

## Installation

1. Clone the repository

```bash
git clone https://github.com/shahzaibkaramat67-coder/Agent_with_functions_flow_with_streamlit.git
cd Agent_with_functions_flow_with_streamlit
```

2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

3. Install dependencies

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root and add the required keys.

Example:

```env
GEMINI_NEW_API_KEY=your_gemini_api_key
GEMINI_API_MODEL=gemini-2.5-flash
TAVILY_API_KEY=your_tavily_api_key
EMBADDING_MODEL_SENTENCE=sentence-transformers/all-MiniLM-L6-v2
```

Notes:

- The app also allows these settings to be entered directly in the Streamlit sidebar.
- The variable name `EMBADDING_MODEL_SENTENCE` appears as written in the code and should be used exactly unless the code is updated.

## Run the App

```bash
streamlit run main.py
```

Then open the URL shown in the terminal, usually `http://localhost:8501`.

## How It Works

1. Upload a document from the sidebar.
2. Click "Build document index" to split and embed the file.
3. Wait for the vector database to be created in `data/chroma_db`.
4. Ask a question in the chat input.
5. The agent selects a tool based on the query:
   - `RAG` if the document is likely relevant
   - `SEARCH` if the answer likely requires live web content
   - `NONE` if no external tool is needed
6. The agent evaluates whether the retrieved information is sufficient.
7. If needed, it creates a new query and continues the loop.
8. The final LLM generates the final answer using the available information.

## Example Workflow

A typical session may look like this:

- User uploads a PDF containing a product specification.
- The document is indexed.
- User asks: "Summarize the key features of this product."
- The agent chooses `RAG` and retrieves the most relevant document chunks.
- The LLM answers from those chunks.

Another example:

- User asks: "What is the latest information about climate policy in Europe?"
- The agent chooses `SEARCH` and calls Tavily.
- It evaluates the search results and composes a final answer.

## Important Notes

- This project relies on external API keys for Gemini and Tavily.
- Local document storage and vector indexing happen at runtime.
- The app is meant for experimentation and custom research workflows rather than as a production-ready product out of the box.
- Some package versions may require Python compatibility checks depending on the environment.

## Use Cases

This project is suitable for:

- document Q&A assistants
- research copilots
- upload-and-query knowledge bases
- web-backed AI assistants
- multi-tool LLM workflows

## License

A license file was not found in the repository. If this project is intended for public distribution, consider adding an open-source license such as MIT or Apache 2.0.

## Summary

This repository is a Python-based AI agent application that blends document retrieval, live web search, and iterative tool-based reasoning inside a Streamlit interface. It is a strong example of a lightweight agentic RAG app built for local question answering and research tasks.

