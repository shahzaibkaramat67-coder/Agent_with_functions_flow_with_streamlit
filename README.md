# Agent with Function Flow with Streamlit

A Python-based research assistant that combines document ingestion, vector retrieval, web search, and agent-style tool routing in a single Streamlit application. The project is designed to help users upload local documents, build a searchable knowledge base, and ask questions that can be answered from either the indexed content or live web results.

This repository demonstrates an agentic RAG workflow: the app analyzes the user request, selects a tool, evaluates whether the information is sufficient, and either produces a final answer or plans the next step. It is especially useful for prototyping document-grounded AI assistants, research copilots, and internal knowledge tools.

## Overview

The application provides a single workspace where users can:

- upload PDF, TXT, or DOCX files
- build a local Chroma vector index from the uploaded document
- ask grounded questions based on the indexed content
- use Tavily for live web search when needed
- inspect the agent's decision path and intermediate logs
- experiment with multi-step reasoning and tool selection logic

## Why this project matters

This project is useful for developers and researchers building:

- document Q&A systems
- retrieval-augmented generation (RAG) pipelines
- local knowledge assistants
- research copilots with web + document integration
- prototype agent workflows with decision-making loops

It is intentionally modular, making it easy to understand how retrieval, tool selection, evaluation, planning, and final answer generation work together in an agentic system.

## Key Features

- Streamlit-based conversational interface
- Support for PDF, TXT, and DOCX ingestion
- Local ChromaDB vector storage and retrieval
- Hugging Face embeddings integration
- Tavily API-powered web search
- Agent loop with tool routing and planning
- Result evaluation before final response generation
- Detailed execution logs for debugging and transparency
- Configuration through environment variables and the app sidebar

## Architecture

The project follows a layered architecture:

1. Frontend and session layer
   - `main.py` handles the Streamlit UI, file uploads, chat flow, and request orchestration.

2. Agent orchestration layer
   - `Agentic_Agent/piplimimg.py` defines the main reasoning loop.
   - It rewrites the user question, chooses a tool, evaluates the result, and decides whether to continue or answer.

3. Tool selection and evaluation layer
   - `function_tool/` contains the decision-making modules:
     - `tool_function.py` chooses the appropriate tool
     - `tool_run.py` executes the selected tool
     - `evaluation.py` checks answer sufficiency
     - `planner.py` decides whether to continue
     - `final_result.py` generates the final answer

4. Retrieval layer
   - `Tools/Rag/system_setup.py` creates the Chroma vector database.
   - `Tools/Rag/retrive.py` loads the index and retrieves relevant document chunks.

5. Search layer
   - `Tools/search/search.py` retrieves live web content through the Tavily API.

6. Model layer
   - `Agentic_Agent/model.py` configures the Gemini model and loads environment values.

7. File ingestion layer
   - `fileLoder/fileLoder.py` loads different document types into LangChain document objects.

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
├── README.md
├── main.py
├── requirements.txt
├── uploads/
├── data/
└── __pycache__/
```

## Tech Stack

- Python 3.10+
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
- python-dotenv
- pydantic
- sentence-transformers

## Prerequisites

Before running the project, make sure you have:

- Python 3.10 or newer
- pip installed
- internet access for model and website retrieval calls
- a Gemini API key
- a Tavily API key if you want web search enabled

## Installation

Clone the repository:

```bash
git clone https://github.com/shahzaibkaramat67-coder/Agent_with_functions_flow_with_streamlit.git
cd Agent_with_functions_flow_with_streamlit
```

Create and activate a virtual environment:

```bash
python -m venv .venv
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

On Windows:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## Environment Variables

Create a `.env` file in the project root with the required environment variables:

```env
GEMINI_NEW_API_KEY=your_gemini_api_key
GEMINI_API_MODEL=gemini-2.5-flash
TAVILY_API_KEY=your_tavily_api_key
EMBADDING_MODEL_SENTENCE=sentence-transformers/all-MiniLM-L6-v2
```

Note: The variable name `EMBADDING_MODEL_SENTENCE` is used by the project as-is, so keep that exact spelling unless you also update the code references.

You can also enter some values directly in the Streamlit sidebar UI when the app is running.

## Running the Application

Start the app with:

```bash
streamlit run main.py
```

Then open the local Streamlit URL shown in the terminal.

## How the App Works

1. Upload a local document in the sidebar.
2. Click "Build document index" to parse and embed the document.
3. Ask a question in the chat interface.
4. The agent picks the best action:
   - `RAG` for document-grounded retrieval
   - `SEARCH` for web search
   - `NONE` when no external tool is needed
5. The returned result is evaluated for completeness.
6. If more information is required, the planner decides on the next action.
7. A final answer is generated and presented to the user.

## Example Use Cases

### Local Knowledge Q&A

- Upload a PDF or internal document.
- Ask: "Summarize the main findings in this document."
- The app retrieves the most relevant chunks and answers from the embedded content.

### Research Assistant

- Ask: "What are the newest developments in AI safety?"
- The app may invoke the search tool and combine external findings with reasoning.

### Multi-Step Tool Reasoning

- Ask a question that needs both context and fresh information.
- The agent can continue iterating through retrieval and search until it has enough data.

## Runtime Behavior and Logs

The app records execution details, including:

- tool selected by the agent
- query sent to the tool
- length of the returned context
- evaluation result
- planner decision
- final response status

This makes the app useful for debugging, demos, and learning how an LLM-driven workflow operates in real time.

## Troubleshooting

### Missing API keys

If you see errors about missing Gemini or Tavily credentials, add them to the `.env` file or enter them in the sidebar before asking questions.

### Document indexing fails

Check that the uploaded file is valid and supported (`.pdf`, `.txt`, `.docx`). If the file is empty or corrupted, the app will not create a usable index.

### Search or RAG does not return useful results

- confirm the embedding model is available and installed
- verify the `data/chroma_db` directory is being created correctly
- check that the document was successfully indexed before asking retrieval-based questions

### Dependency issues

If package conflicts occur, recreate the virtual environment and run:

```bash
pip install -r requirements.txt
```

## Repository Notes

- The project is designed as a learning and prototyping repository.
- The agent loop is intentionally transparent and easy to inspect.
- The app depends on external API access for Gemini and Tavily.
- Some environments may require dependency version adjustments depending on Python and system libraries.

## License

This repository does not currently include a license file. If you plan to distribute or publish the project publicly, it is recommended to add an open-source license such as MIT.

## Contributing

Contributions are welcome. Possible areas to extend the project include:

- improved prompt design
- broader document format support
- better retrieval ranking and filtering
- more agent tools and workflows
- enhanced UI and debugging views

## Contact and Project Link

Repository:

https://github.com/shahzaibkaramat67-coder/Agent_with_functions_flow_with_streamlit

## Summary

This repository is a practical example of an AI research assistant built with Python and Streamlit. It combines document ingestion, local vector retrieval, live web search, and agent-style tool reasoning into a single interactive application. It is a strong foundation for building more advanced AI assistants, internal enterprise Q&A tools, or custom research copilots.
