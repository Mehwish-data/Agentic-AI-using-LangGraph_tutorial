from __future__ import annotations
from typing import List
from ..state import AppState

def run(state: AppState) -> AppState:
    topics = sorted(state.get("topics", []), key=lambda t: t.get("score", 0), reverse=True)
    lines: List[str] = []
    lines.append(f"# Topic Recommendations for {state['discipline']} — {state['region']}")
    lines.append("")
    lines.append("Top picks are ranked by novelty, policy demand, data feasibility, method fit, and timeliness.\n")
    for i, t in enumerate(topics, 1):
        lines.append(f"## {i}. {t['title']}")
        lines.append(f"**Score:** {t.get('score', 0)}")
        lines.append("")
        lines.append(f"**Gap rationale:** {t.get('gap_rationale','')}")
        lines.append("")
        if t.get("policy_links"):
            lines.append("**Policy links:**")
            for pl in t["policy_links"]:
                src = pl.get("source", ""); sec = pl.get("section", ""); url = pl.get("url") or ""
                if url:
                    lines.append(f"- {src} — *{sec}* ({url})")
                else:
                    lines.append(f"- {src} — *{sec}*")
            lines.append("")
        if t.get("methods"):
            lines.append("**Suggested methods:** " + ", ".join(t["methods"]))
        if t.get("datasets"):
            lines.append("**Candidate datasets:** " + ", ".join(t["datasets"]))
        if t.get("risks"):
            lines.append("**Risks & mitigations:**")
            for r in t["risks"]:
                lines.append(f"- {r}")
        if t.get("starter_refs"):
            lines.append("**Starter references:**")
            for rp in t["starter_refs"][:8]:
                lines.append(f"- {rp.get('title')} ({rp.get('year')}) — {rp.get('url')}")
        lines.append("")
    state["markdown_brief"] = "\n".join(lines)
    return state
