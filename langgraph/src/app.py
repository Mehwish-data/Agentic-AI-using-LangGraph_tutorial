from __future__ import annotations
from typing import Dict, Any, Optional, List
from fastapi import FastAPI
from pydantic import BaseModel, Field
from .state import AppState
from .graph import build_graph

class RunRequest(BaseModel):
    discipline: str = Field(example="Economics")
    region: str = Field(example="South Punjab, Pakistan")
    subdomain: Optional[str] = Field(default=None, example="women entrepreneurship")
    constraints: Dict[str, str] = Field(default_factory=dict)

class RunResponse(BaseModel):
    topics: List[Dict[str, Any]]
    markdown_brief: str
    quality_notes: List[str]

app = FastAPI(title="Research Topic & Policy Gap Recommender — LangGraph + Gemini")
GRAPH = build_graph()

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/run", response_model=RunResponse)
def run(req: RunRequest):
    state: AppState = {
        "discipline": req.discipline,
        "region": req.region,
        "subdomain": req.subdomain,
        "constraints": req.constraints or {},
        "papers": [],
        "indicators": [],
        "policy_docs": [],
        "themes": [],
        "gaps": [],
        "topics": [],
        "quality_notes": [],
        "markdown_brief": "",
        "next_action": "start",
    }
    out = GRAPH.invoke(state)
    return RunResponse(
        topics=out.get("topics", []),
        markdown_brief=out.get("markdown_brief", ""),
        quality_notes=out.get("quality_notes", []),
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("src.app:app", host="0.0.0.0", port=8000, reload=True)
