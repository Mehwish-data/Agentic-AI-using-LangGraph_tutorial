from __future__ import annotations
from ..state import AppState

def run(state: AppState) -> AppState:
    state["discipline"] = state["discipline"].strip().title()
    state["region"] = state["region"].strip()
    if state.get("subdomain"):
        state["subdomain"] = state["subdomain"].strip().lower()
    state["next_action"] = "normalized"
    return state
