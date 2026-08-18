from dataclasses import dataclass
from typing import Dict, List


@dataclass
class OverallStats:

    total_attempts: int

    accepted_attempts: int

    rejected_attempts: int

    unique_problems_attempted: int

    unique_problems_solved: int

    acceptance_rate: float


@dataclass
class DifficultyStats:

    difficulty: str

    total_attempts: int

    accepted_attempts: int

    unique_problems_solved: int

    acceptance_rate: float


@dataclass
class TopicStats:

    topic: str

    total_attempts: int

    accepted_attempts: int

    unique_problems_solved: int

    acceptance_rate: float