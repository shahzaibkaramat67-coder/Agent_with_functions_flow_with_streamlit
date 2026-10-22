from Tools.search.search import search


def Tool_run(tool_name, query):
    tool_name = (tool_name or "").lower()

    try:
        if tool_name == "search":
            return search(query)
        if tool_name == "rag":
            from Tools.Rag.retrive import retriver_ChromaDB

            return retriver_ChromaDB(query)
        if tool_name == "none":
            return "none"
        return "none"
    except Exception as exc:
        return f"Tool execution failed: {str(exc)}"
