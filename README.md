# Agent with Function Flow with Streamlit

A Python-based AI research assistant built with Streamlit, LangChain, and Gemini-powered reasoning. The application lets users upload documents, build a local vector index, and ask questions that can be answered using document retrieval, web search, or a multi-step agent workflow.

This project demonstrates a practical "agentic RAG" pattern: the app selects tools, evaluates whether enough information has been gathered, and plans follow-up actions before returning a final response.

## Demo / Overview

The application provides a single research workspace where users can:

- upload PDFs, TXT, or DOCX files
- create a searchable ChromaDB vector index
- ask questions grounded in the uploaded document
- perform live web searches with Tavily
- let an AI agent reason across tools and decide the next step
- inspect logs and intermediate agent decisions in the app UI

## Why This Project

This project is useful for anyone building:

- document-based AI assistants
- research copilots
- local knowledge-base Q&A apps
- tool-using LLM workflows
- prototype agentic systems for search + retrieval + reasoning

It is intentionally built as a modular learning project, making it easy to understand how tool routing, evaluation, planning, and retrieval fit together in a real application.

## Key Features

- Streamlit chat-based user interface
- PDF, TXT, and DOCX ingestion
- Local vector database indexing using Chroma
- Hugging Face embeddings support
- Tavily-based web search integration
- Agentic workflow with tool selection and evaluation
- Multi-step reasoning loop with planner logic
- Detailed execution logs for transparency
- Environment-based API configuration

## System Architecture

The project follows a layered architecture:

1. Frontend layer
   - `main.py` handles the Streamlit UI and user interaction.

2. Agent orchestration layer
   - `Agentic_Agent/piplimimg.py` manages the main reasoning loop.
   - It rewrites the user question, selects a tool, evaluates results, retries when needed, and produces the final answer.

3. Tool layer
   - `function_tool/` contains modules for tool selection, execution, evaluation, planning, and final answer generation.

4. Retrieval layer
   - `Tools/Rag/` handles document chunking, embedding, retrieval, and grounded answer generation.

5. Search layer
   - `Tools/search/search.py` connects to Tavily to fetch live results for web-based questions.

6. Model layer
   - `Agentic_Agent/model.py` configures the Gemini LLM client and key handling.

## Repository Structure

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
├── uploads/
└── data/
```

## Core Components

### 1. Streamlit App
File: `main.py`

The app provides:

- sidebar configuration for Gemini model and API keys
- file upload support for local knowledge indexing
- a chat interface for question answering
- status and log tracking for each request

### 2. Agent Entry Point
File: `Agentic_Agent/piplimimg.py`

This is the heart of the project. It follows a loop similar to:

- rewrite the user request
- choose a tool (`SEARCH`, `RAG`, or `NONE`)
- run the chosen tool
- evaluate whether enough context has been found
- either finalize the answer or plan another step

### 3. Tool Selection and Evaluation
Files in `function_tool/`

- `tool_function.py`: determines which tool is best suited for the request
- `tool_run.py`: executes the selected tool
- `evaluation.py`: checks whether the returned information is sufficient
- `planner.py`: decides whether the next action should be another search or a finish
- `final_result.py`: produces the final answer with the LLM

### 4. Document Loader
File: `fileLoder/fileLoder.py`

Supported inputs:

- PDF
- TXT
- DOCX
- URL-based web pages

### 5. RAG Layer
Files in `Tools/Rag/`

- `system_setup.py` creates the Chroma vector store
- `retrive.py` loads the index, retrieves relevant chunks, and builds a grounded answer prompt

### 6. Search Layer
File: `Tools/search/search.py`

This module calls the Tavily API and turns search results into a usable context string for the agent.

### 7. LLM Model Setup
File: `Agentic_Agent/model.py`

Responsible for:

- loading API keys from environment variables
- resolving the Gemini model name
- creating the LLM instance used by the agent

## Tech Stack

- Python
- Streamlit
- LangChain
- LangChain Community
- LangChain Google GenAI
- LangChain Hugging Face
- ChromaDB
- FAISS
- Hugging Face Embeddings
- Tavily API
- Google Generative AI
- PyPDF
- python-docx
- pydantic
- dotenv
- sentence-transformers

## Prerequisites

Before running the project, ensure the following are installed:

- Python 3.10+
- pip
- Access to internet for external APIs
- A valid Gemini API key
- A valid Tavily API key if you want web search enabled

## Installation

Clone the repository:

```bash
git clone https://github.com/shahzaibkaramat67-coder/Agent_with_functions_flow_with_streamlit.git
cd Agent_with_functions_flow_with_streamlit
```

Create and activate a virtual environment:

```bash
python -m venv venv
source venv/bin/activate
```

On Windows:

```bash
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root:

```env
GEMINI_NEW_API_KEY=your_gemini_api_key
GEMINI_API_MODEL=gemini-2.5-flash
TAVILY_API_KEY=your_tavily_api_key
EMBADDING_MODEL_SENTENCE=sentence-transformers/all-MiniLM-L6-v2
```

You can also enter some of these values directly in the Streamlit sidebar UI.

## Running the Application

Start the app with:

```bash
streamlit run main.py
```

Then open the local Streamlit URL shown in the terminal.

## How the App Works

1. Upload a document in the sidebar.
2. Click the "Build document index" button.
3. The app converts the document into text chunks and stores embeddings in Chroma.
4. Ask a question in the chat interface.
5. The agent decides whether the tool should be:
   - `RAG` for document-grounded lookups
   - `SEARCH` for live web search
   - `NONE` when no external tool is required
6. The result is evaluated to determine if the answer is sufficient.
7. If more information is needed, the planner selects a new action.
8. A final answer is generated and returned to the user.

## Example Use Cases

### Local knowledge Q&A

- Upload an internal document or technical PDF.
- Ask: "Summarize the main risks described in this document."
- The app retrieves the most relevant document chunks and answers from them.

### Research assistant

- Ask: "What are the latest developments in AI safety?"
- The agent chooses the web search tool.
- It gathers fresh results and builds a response from the returned content.

### Multi-tool reasoning

The system can alternate between retrieval and search when a single source is not enough to fully answer a question.

## Outputs and Logs

The app records execution details including:

- tool used
- query sent to the tool
- result length
- evaluation judgment
- planner decision
- final answer status

This makes the project easier to debug and understand while it is running.

## Notes

- The app depends heavily on external API access for Gemini and Tavily.
- Local indexing is performed at runtime and stored under the project data directories.
- This is a research and prototyping project and may require environment-specific fixes depending on the machine and package versions.
- Some dependencies may need version pinning depending on your Python environment.

## License

This repository does not currently include a license file. If you plan to distribute or publish the project publicly, it is recommended to add an appropriate open-source license such as MIT or Apache 2.0.

## Contributing

Contributions are welcome. If you want to extend the project:

- add new tools to the agent workflow
- improve the retrieval quality
- add better prompt engineering
- add support for more document formats
- improve UI/UX and logging

## Project Summary

This repository is a lightweight but realistic example of an AI agent application built for research and document-grounded Q&A. It combines:

- document ingestion
- vector retrieval
- LLM prompting
- web search
- tool reasoning
- orchestrated agent decision-making

It is well-suited as a foundation for building more advanced AI assistants, internal knowledge tools, or RAG-powered chat systems.

## Contact

For questions or collaboration, use the repository on GitHub:

https://github.com/shahzaibkaramat67-coder/Agent_with_functions_flow_with_streamlit

