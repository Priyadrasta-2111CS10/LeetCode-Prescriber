from dataclasses import dataclass, field
from typing import Any, Dict, List


@dataclass
class AnalyticsSnapshot:

    username: str

    overall: Dict[str, Any]

    difficulty: List[Dict[str, Any]]

    topics: List[Dict[str, Any]]

    weak_topics: List[Dict[str, Any]]

    submission_status: List[Dict[str, Any]]