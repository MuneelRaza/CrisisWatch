from typing import Annotated, Sequence
from langgraph.graph import MessagesState
from langgraph.prebuilt import ToolNode
from typing_extensions import TypedDict
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import END, StateGraph, START
from langgraph.graph.message import add_messages
from langchain_core.messages import BaseMessage, SystemMessage

import sys
import os

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path)) 


if project_root not in sys.path:
    sys.path.insert(0, project_root)


from utils.import_llm import llama_model
from agent.exa_tool import exa_search_tool
from agent._system_prompt import CRISIS_CONTEXT_PROMPT



class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]
    intent: str


llm_with_tools = llama_model.bind_tools([exa_search_tool])


def agent(state: MessagesState):
    messages = [SystemMessage(content=CRISIS_CONTEXT_PROMPT)] + state["messages"]
    result = llm_with_tools.invoke(messages)

    return {"messages": [result]}


def tools_condition(state: AgentState) -> str:
    messages = state.get("messages", [])
    if messages and hasattr(messages[-1], "tool_calls") and messages[-1].tool_calls:
        return "tool_used"
    return "final_answer"

def crisis_agent():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent-node", agent)
    workflow.add_node("tools", ToolNode([exa_search_tool]))

    workflow.add_edge(START, "agent-node")

    workflow.add_conditional_edges(
        "agent-node",
        tools_condition,
        {
            "tool_used": "tools",
            "final_answer": END
        }
    )

    workflow.add_edge("tools", "agent-node")

    memory = MemorySaver()
    react_graph_memory = workflow.compile(checkpointer=memory)
    return react_graph_memory

