from typing import Literal, Optional

from pydantic import BaseModel, Field


class ProblemRecommendation(BaseModel):

    title: str

    # NOT part of the LLM's response schema requirement (default=None
    # means it's optional in the generated JSON) — the model is
    # unreliable at reproducing exact URL slugs character-for-character.
    # This gets populated server-side in practice_plan_service.py by
    # looking up the matching candidate's real title_slug, after the
    # existing title-based validation already confirms which candidate
    # this recommendation corresponds to.
    title_slug: Optional[str] = None

    reason: str

    priority: Literal[
        "HIGH",
        "MEDIUM",
        "LOW",
    ]

    suggested_order: int


class PracticePlan(BaseModel):

    topic: str

    goal: str

    problems: list[
        ProblemRecommendation
    ]


class PracticePlanBatch(BaseModel):
    """
    Wraps multiple PracticePlans returned from a single LLM call — lets
    AIProblemRecommender.recommend_batch() cover every weak topic in one
    request instead of one request per topic.
    """

    plans: list[PracticePlan]