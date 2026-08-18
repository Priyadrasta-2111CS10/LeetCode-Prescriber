from dataclasses import dataclass
from typing import List, Optional


@dataclass
class User:
    username: str

    ranking: Optional[int] = None
    real_name: Optional[str] = None
    about_me: Optional[str] = None
    school: Optional[str] = None
    country_name: Optional[str] = None
    company: Optional[str] = None
    job_title: Optional[str] = None

    github_url: Optional[str] = None
    twitter_url: Optional[str] = None
    linkedin_url: Optional[str] = None

    avatar_url: Optional[str] = None

    websites: Optional[List[str]] = None
    skill_tags: Optional[List[str]] = None

    reputation: Optional[int] = None
    solution_count: Optional[int] = None
    category_discuss_count: Optional[int] = None