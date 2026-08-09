from langchain_core.language_models.chat_models import BaseChatModel
from langgraph.graph import END, START, StateGraph

from resbot.graph.nodes import build_analyze_node, extract_docs, load_docs
from resbot.graph.state import AgentState


def build_agent_graph(llm: BaseChatModel):
    graph = StateGraph(AgentState)

    graph.add_node("load_docs", load_docs)
    graph.add_node("extract_docs", extract_docs)
    graph.add_node("analyze", build_analyze_node(llm))

    graph.add_edge(START, "load_docs")
    graph.add_edge("load_docs", "extract_docs")
    graph.add_edge("extract_docs", "analyze")
    graph.add_edge("analyze", END)

    return graph.compile()

