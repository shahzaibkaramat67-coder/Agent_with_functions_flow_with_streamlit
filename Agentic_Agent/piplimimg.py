from typing import Callable

from function_tool.updateQuery import updateQuery
from function_tool.final_result import final_result
from function_tool.tool_function import Tool_function
from function_tool.evaluation import evaluation
from function_tool.planner import Planner
from function_tool.tool_run import Tool_run


def entryPoint(user_input, log_callback: Callable[[str], None] | None = None):
    def log(message):
        if log_callback is not None:
            log_callback(message)

    print("here we enter in the model")
    log("Rewriting the question for the agent.")

    update_query = updateQuery(user_input)

    max_iteration = 3

    steps = []

    print("update_query", update_query)
    log(f"Question prepared: {update_query}")

    for iteration in range(max_iteration):

        print(f"======== iteration NO {iteration} ========")
        log(f"Iteration {iteration + 1} of {max_iteration}: selecting a tool.")

        Tool_info = Tool_function(update_query)

        tool_name = Tool_info["tool_name"]
        query = Tool_info["query"]
        log(f"Selected {tool_name} for: {query}")

        tool_result = Tool_run(tool_name, query)
        log(f"{tool_name} returned {len(str(tool_result))} characters of context.")

        current_step = {
            "iteration": iteration + 1,
            "updated_query": update_query,
            "tool_name": tool_name,
            "tool_query": query,
            "tool_result": tool_result,
        }

        if tool_result == "none":
            steps.append(current_step)
            log("No external tool was needed; preparing the final answer.")

            answer = final_result(update_query, "")
            log("Final answer ready.")

            return {"final_answer": answer, "steps": steps, "status": "completed"}

        evaluation_result = evaluation(update_query, tool_result)

        current_step["evaluation"] = evaluation_result

        print("evaluation_result", evaluation_result)
        log(
            "Evaluation: "
            + (
                "enough information was found."
                if evaluation_result["enough_information"]
                else "additional information is needed."
            )
        )

        steps.append(current_step)

        if evaluation_result["enough_information"]:
            log("Preparing the final answer.")

            answer = final_result(update_query, tool_result)
            log("Final answer ready.")

            return {"final_answer": answer, "steps": steps, "status": "completed"}

        print("Running Planner...")
        log("Planning the next step.")

        plan = Planner(update_query, tool_result, evaluation_result["reason"])

        print("planner_result", plan)
        log(f"Planner chose {plan['action']}.")

        current_step["planner"] = plan

        action = plan["action"]

        if action == "FINISH":
            log("Preparing the final answer from the available information.")

            answer = final_result(update_query, tool_result)
            log("Final answer ready.")

            return {"final_answer": answer, "steps": steps, "status": "completed"}

        if action in ["SEARCH", "RAG"]:

            update_query = plan["query"]
            log(f"Next query: {update_query}")

            continue

    log("The iteration limit was reached before enough information was found.")
    return {
        "final_answer": "Unable to gather enough information.",
        "steps": steps,
        "status": "failed",
    }


# from function_tool.updateQuery import updateQuery

# from function_tool.final_result import final_result

# from function_tool.tool_function import Tool_function
# from function_tool.evaluation import evaluation

# from function_tool.planner import Planner
# from function_tool.tool_run import Tool_run
# import json

# import json

# # from Agentic_Agent.model import llm


# def entryPoint(user_input):
#     print("here we eenter in the model")
#     update_query = updateQuery(user_input)

#     max_itration = 3

#     print("update_query", update_query)
#     for itrate in range(max_itration):

#         print(f"======== itration NO {itrate} =======")
#         Tool_info = Tool_function(update_query)
#         # tool_result_json = json.loads(tool_result)

#         tool_name = Tool_info["tool_name"]
#         query = Tool_info["query"]
#         # function_tool
#         tool_result = Tool_run(tool_name, query)

#         if tool_result == "none":
#             return final_result(update_query)

#         evaluation_result = evaluation(update_query, tool_result)

#         print("evaluation_result", evaluation_result)

#         if evaluation_result["enough_information"]:
#             return final_result(update_query, tool_result)

#         print("Running Planner...")

#         plan = Planner(update_query, tool_result, evaluation_result["reason"])
#         print("planner_result", plan)

#         action = plan["action"]

#         if action == "FINISH":
#             return final_result(update_query, tool_result)

#         if action in ["SEARCH", "RAG"]:
#             update_query = plan["query"]
#             continue

#     return "Unable to gather enough information."
