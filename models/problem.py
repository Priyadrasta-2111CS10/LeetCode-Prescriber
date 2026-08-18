from dataclasses import dataclass
from typing import List, Optional


@dataclass
class Problem:
    question_id: str
    frontend_id: str

    title: str
    title_slug: str

    difficulty: str

    topics: List[str]

    is_paid_only: bool = False

    acceptance_rate: Optional[float] = None