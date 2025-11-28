from __future__ import annotations
from typing import TypedDict, List, Dict, Optional, Any

class Paper(TypedDict):
    id: str
    title: str
    year: int
    url: str
    abstract: Optional[str]
    citations: int
    fields: List[str]
    region_mentioned: bool

class Indicator(TypedDict):
    code: str
    name: str
    value: Optional[float]
    year: Optional[int]

class PolicyRef(TypedDict):
    source: str
    section: str
    excerpt: str
    url: Optional[str]

class TopicRec(TypedDict):
    title: str
    gap_rationale: str
    policy_links: List[PolicyRef]
    methods: List[str]
    datasets: List[str]
    risks: List[str]
    starter_refs: List[Paper]
    score: float

class AppState(TypedDict):
    discipline: str
    region: str
    subdomain: Optional[str]
    constraints: Dict[str, str]

    papers: List[Paper]
    indicators: List[Indicator]
    policy_docs: List[PolicyRef]

    themes: List[str]
    gaps: List[str]
    topics: List[TopicRec]
    quality_notes: List[str]

    markdown_brief: str
    next_action: str
