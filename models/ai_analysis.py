from typing import Literal

from pydantic import BaseModel, Field


class TopicRecommendation(BaseModel):

    topic: str = Field(
        description="LeetCode topic to practice"
    )

    reason: str = Field(
        description="Why this topic should be prioritized"
    )

    priority: Literal[
        "HIGH",
        "MEDIUM",
        "LOW",
    ]


class PracticeRecommendation(BaseModel):

    summary: str = Field(
        description="Short overall assessment"
    )

    strengths: list[str]

    weaknesses: list[str]

    recommendations: list[
        TopicRecommendation
    ]