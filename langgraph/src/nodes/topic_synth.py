from __future__ import annotations
from typing import List
import os, re
import json
import google.generativeai as genai

from ..state import AppState, TopicRec, PolicyRef
from ..scoring import (
    normalize_region, novelty_score, policy_demand_score,
    data_feasibility_score, method_fit_score, timeliness_score
)
from ..prompts import TOPIC_SYNTH_PROMPT

# Configure Gemini if key exists
API_KEY = os.getenv("GOOGLE_API_KEY")
if API_KEY:
    genai.configure(api_key=API_KEY)

def _offline_topics(state: AppState) -> List[TopicRec]:
    region = state["region"]
    disc = state["discipline"]
    policies = state.get("policy_docs", [])
    inds = state.get("indicators", [])

    themes = []
    for g in state.get("gaps", []):
        m = re.search(r"'([^']+)'", g)
        if m:
            themes.append(m.group(1))
    if not themes:
        themes = state.get("themes", [])[:3]

    out: List[TopicRec] = []
    for th in themes[:3]:
        title = f"{th.title()} in {region}: Evidence for {disc} Policy"
        gap = (
            f"Global literature covers {th}, but subnational evidence for {region} is scarce. "
            f"This project addresses that gap using recent indicators and secondary data."
        )
        pol_links: List[PolicyRef] = policies[:2] if len(policies) >= 2 else policies
        methods = ["Difference-in-differences", "Panel regression", "Thematic interviews"]
        datasets = [
            "Household/Enterprise Survey (e.g., PSLM)",
            "District-level broadband/ICT coverage",
            "SME/Youth program administrative data (if accessible)",
        ]
        risks = [
            "Restricted access to admin data",
            "Measurement error in self-reports",
            "Short timeline limits fieldwork",
        ]
        starters = state.get("papers", [])[:6]

        nov = 0.6
        pol = policy_demand_score(th, policies)
        dat = data_feasibility_score(th, inds, state.get("papers", []))
        mfit = method_fit_score(state.get("constraints", {}))
        time = timeliness_score(inds)
        score = 0.35*nov + 0.25*pol + 0.20*dat + 0.10*mfit + 0.10*time

        out.append({
            "title": title,
            "gap_rationale": gap,
            "policy_links": pol_links,
            "methods": methods,
            "datasets": datasets,
            "risks": risks,
            "starter_refs": starters,
            "score": round(float(score), 3),
        })
    return out

def run(state: AppState) -> AppState:
    topics: List[TopicRec] = []
    if API_KEY:
        try:
            model = genai.GenerativeModel("gemini-1.5-flash")
            payload = {
                "discipline": state["discipline"],
                "region": state["region"],
                "gaps": state.get("gaps", []),
                "indicators": state.get("indicators", []),
                "policies": state.get("policy_docs", []),
                "papers": [p["title"] for p in state.get("papers", [])[:10]],
            }
            prompt = TOPIC_SYNTH_PROMPT + "\n\nINPUT:\n" + json.dumps(payload, ensure_ascii=False)
            resp = model.generate_content(prompt)
            text = resp.text or ""
            m = re.search(r"\{[\s\S]*\}$", text.strip())
            if m:
                data = json.loads(m.group(0))
                candidate = data.get("topics", [])
                if candidate:
                    topics = candidate
        except Exception:
            topics = []
    if not topics:
        topics = _offline_topics(state)
    state["topics"] = topics
    state["next_action"] = "finalize"
    return state
