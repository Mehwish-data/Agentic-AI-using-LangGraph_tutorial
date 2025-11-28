from __future__ import annotations
from ..state import AppState

def run(state: AppState) -> AppState:
    if len(state["papers"]) < 3:
        state["quality_notes"].append("Low literature volume; consider broadening subdomain.")
    if len(state["indicators"]) < 2:
        state["quality_notes"].append("Insufficient indicators; add World Bank or local stats.")
    return state
