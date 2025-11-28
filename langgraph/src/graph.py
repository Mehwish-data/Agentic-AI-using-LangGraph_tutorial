from __future__ import annotations
from langgraph.graph import StateGraph, END
from .state import AppState
from .nodes import normalize, retrieve_policy, retrieve_lit, retrieve_indicators, theme_miner, gap_analyzer, feasibility, topic_synth, packager

def build_graph():
    g = StateGraph(AppState)

    g.add_node("normalize", normalize.run)
    g.add_node("retrieve_policy", retrieve_policy.run)
    g.add_node("retrieve_lit", retrieve_lit.run)
    g.add_node("retrieve_indicators", retrieve_indicators.run)
    g.add_node("theme_miner", theme_miner.run)
    g.add_node("gap_analyzer", gap_analyzer.run)
    g.add_node("feasibility", feasibility.run)
    g.add_node("topic_synth", topic_synth.run)
    g.add_node("packager", packager.run)

    g.set_entry_point("normalize")
    g.add_edge("normalize", "retrieve_policy")
    g.add_edge("retrieve_policy", "retrieve_lit")
    g.add_edge("retrieve_lit", "retrieve_indicators")
    g.add_edge("retrieve_indicators", "theme_miner")
    g.add_edge("theme_miner", "gap_analyzer")
    g.add_edge("gap_analyzer", "feasibility")

    def _route(state: AppState) -> str:
        if any("Low" in q for q in state.get("quality_notes", [])):
            return "loop"
        return "go"

    g.add_conditional_edges("feasibility", _route, {"loop": "theme_miner", "go": "topic_synth"})
    g.add_edge("topic_synth", "packager")
    g.add_edge("packager", END)

    return g.compile()
