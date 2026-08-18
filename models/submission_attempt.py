from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class SubmissionAttempt:

    leetcode_submission_id: str

    username: str

    title: str
    title_slug: str

    status: str

    language: Optional[str]

    runtime: Optional[str]

    memory: Optional[str]

    submitted_at: datetime