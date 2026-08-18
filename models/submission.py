from dataclasses import dataclass
from datetime import datetime


@dataclass
class Submission:
    id: str

    title: str
    title_slug: str

    submitted_at: datetime

    username: str