from datetime import datetime
from pathlib import Path
from typing import Callable
import os

import streamlit as st
from dotenv import load_dotenv

from Agentic_Agent.piplimimg import entryPoint
from fileLoder.fileLoder import file_loaders

load_dotenv()
os.environ["USER_AGENT"] = "my-streamlit-app"


def ensure_api_keys():
    if st.session_state.get("gemini_api_key"):
        os.environ["GEMINI_NEW_API_KEY"] = st.session_state.gemini_api_key.strip()
    gemini_model = st.session_state.get("gemini_model", "").strip()
    if gemini_model:
        os.environ["GEMINI_API_MODEL"] = gemini_model
    else:
        os.environ.pop("GEMINI_API_MODEL", None)
    if st.session_state.get("tavily_api_key"):
        os.environ["TAVILY_API_KEY"] = st.session_state.tavily_api_key.strip()
    if st.session_state.get("embedding_model"):
        os.environ["EMBADDING_MODEL_SENTENCE"] = st.session_state.embedding_model.strip()


def run_query(question: str, log_callback: Callable[[str], None] | None = None):
    try:
        return entryPoint(question, log_callback=log_callback)
    except Exception as exc:
        if log_callback is not None:
            log_callback(f"Run failed: {exc}")
        return {
            "final_answer": f"The agent could not complete this request: {exc}",
            "steps": [],
            "status": "failed",
        }


def append_log(message: str, placeholder):
    timestamp = datetime.now().strftime("%H:%M:%S")
    st.session_state.last_logs.append(f"{timestamp}  {message}")
    timeline = []
    last_index = len(st.session_state.last_logs) - 1
    for index, entry in enumerate(st.session_state.last_logs):
        event_time, separator, event_message = entry.partition("  ")
        if not separator:
            event_message = event_time
            event_time = ""
        icon = ":material/pending:" if index == last_index else ":material/check_circle:"
        timestamp_label = f"`{event_time}` " if event_time else ""
        timeline.append(f"{icon} {timestamp_label}{event_message}")
    placeholder.markdown("\n\n".join(timeline))


def main():
    st.set_page_config(
        page_title="Agent workspace",
        page_icon=":material/psychology:",
        layout="wide",
    )

    st.session_state.setdefault("messages", [])
    st.session_state.setdefault("index_ready", False)
    st.session_state.setdefault("last_logs", [])

    with st.sidebar:
        st.title("Agent workspace", anchor=False)
        st.caption("Research, retrieve, and reason in one place.")

        st.subheader("Knowledge base", icon=":material/database:")
        with st.container(border=True):
            uploaded_file = st.file_uploader(
                "Add a document",
                type=["pdf", "txt", "docx"],
                help="Build a searchable index from a PDF, text file, or Word document.",
            )
            if uploaded_file is not None:
                st.caption(f"Selected: {uploaded_file.name}")

            if st.button(
                "Build document index",
                icon=":material/drive_folder_upload:",
                width="stretch",
                disabled=uploaded_file is None,
            ):
                st.session_state.last_logs = []
                with st.status("Building document index", expanded=True) as status:
                    log_placeholder = st.empty()
                    append_log(f"Reading {uploaded_file.name}", log_placeholder)
                    try:
                        save_dir = Path("uploads")
                        save_dir.mkdir(exist_ok=True)
                        file_path = save_dir / Path(uploaded_file.name).name
                        file_path.write_bytes(uploaded_file.getvalue())

                        documents = file_loaders(str(file_path))
                        if not documents:
                            raise ValueError(
                                "No readable content found. Check that the document is valid."
                            )

                        append_log(
                            f"Loaded {len(documents)} document page(s); creating vector index.",
                            log_placeholder,
                        )
                        from Tools.Rag.system_setup import createChromaDB

                        createChromaDB(documents)
                        st.session_state.index_ready = True
                        append_log("Document index is ready.", log_placeholder)
                        status.update(
                            label="Document index is ready",
                            state="complete",
                            expanded=False,
                        )
                    except Exception as exc:
                        append_log(f"Indexing failed: {exc}", log_placeholder)
                        status.update(
                            label="Document indexing failed",
                            state="error",
                            expanded=True,
                        )
                        st.error(f"Could not index the document: {exc}")

        if st.session_state.index_ready:
            st.badge(
                "Document search ready",
                icon=":material/check_circle:",
                color="green",
            )
        else:
            st.caption("No document indexed in this session.")

        with st.expander("Configuration", icon=":material/tune:", expanded=True):
            st.text_input(
                "Gemini model",
                value=(
                    os.getenv("GEMINI_API_MODEL")
                    or os.getenv("GEMINI_API_MODEL_LITE")
                    or "gemini-2.5-flash"
                ),
                help="Enter the Gemini model name to use, such as gemini-2.5-flash.",
                key="gemini_model",
            )
            st.text_input(
                "Gemini API key",
                value=os.getenv("GEMINI_NEW_API_KEY", ""),
                type="password",
                key="gemini_api_key",
            )
            st.text_input(
                "Tavily API key",
                value=os.getenv("TAVILY_API_KEY", ""),
                type="password",
                key="tavily_api_key",
            )
            st.text_input(
                "Embedding model",
                value=os.getenv(
                    "EMBADDING_MODEL_SENTENCE",
                    "sentence-transformers/all-MiniLM-L6-v2",
                ),
                key="embedding_model",
            )
        ensure_api_keys()

        st.caption("API keys stay private to this app session.")

    st.title("Your AI research desk", icon=":material/auto_awesome:")
    st.caption(
        "Ask a question to start. The agent can search the web or use your indexed document."
    )

    st.subheader("Conversation", icon=":material/forum:")

    if not st.session_state.messages:
        with st.container(border=True):
            st.markdown("**Start with a question**")
            st.caption(
                "Try asking for a summary, a comparison, or an answer "
                "grounded in your uploaded document."
            )

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            if message["role"] == "assistant" and message.get("status") == "failed":
                st.error(message["content"])
            else:
                st.markdown(message["content"])
            if message["role"] == "assistant" and (
                message.get("logs") or message.get("steps")
            ):
                with st.expander("View run details"):
                    if message.get("logs"):
                        st.markdown("\n\n".join(
                            f":material/check_circle: {entry}"
                            for entry in message["logs"]
                        ))
                    if message.get("steps"):
                        st.caption("Agent steps")
                        st.json(message["steps"])

    question = st.chat_input(
        "Ask a question about your document or the web",
        submit_mode="disable",
    )
    if question:
        st.session_state.messages.append({"role": "user", "content": question})
        with st.chat_message("user"):
            st.markdown(question)

        st.session_state.last_logs = []
        with st.chat_message("assistant"):
            with st.status("Working through your question", expanded=True) as status:
                log_placeholder = st.empty()
                append_log("Starting agent workflow.", log_placeholder)
                result = run_query(
                    question,
                    log_callback=lambda message: append_log(
                        message, log_placeholder
                    ),
                )
                answer = str(result.get("final_answer", "No answer was returned."))
                failed = result.get("status") == "failed"
                status.update(
                    label=(
                        "The request could not be completed"
                        if failed
                        else "Answer ready"
                    ),
                    state="error" if failed else "complete",
                    expanded=failed,
                )

            if failed:
                st.error(answer)
            else:
                st.markdown(answer)

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
                "logs": list(st.session_state.last_logs),
                "steps": result.get("steps", []),
                "status": result.get("status", "completed"),
            }
        )


if __name__ == "__main__":
    main()
