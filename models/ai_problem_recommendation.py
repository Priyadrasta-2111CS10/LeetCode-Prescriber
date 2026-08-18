from typing import Literal

from pydantic import BaseModel, Field


class ProblemRecommendation(BaseModel):

    title: str

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