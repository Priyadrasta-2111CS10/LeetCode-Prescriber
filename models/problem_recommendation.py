from dataclasses import dataclass
from typing import List


@dataclass
class ProblemCandidate:

    problem_id: int

    title: str

    title_slug: str

    difficulty: str

    topics: List[str]

    previous_attempts: int

    previous_accepted_attempts: int

    similarity: float

    last_attempted_at: object | None