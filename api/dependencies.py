import os

from dotenv import load_dotenv

load_dotenv()

from db import (
    Database,
    UserRepository,
    ProblemRepository,
    SubmissionAttemptRepository,
    SubmissionRepository,
    SyncMetadataRepository,
)

from leetcode_client import LeetCodeClient

from services.sync_service import SyncService


database = Database()

user_repository = UserRepository(database)

problem_repository = ProblemRepository(database)

submission_attempt_repository = SubmissionAttemptRepository(database)

submission_repository = SubmissionRepository(database)


sync_metadata_repository = SyncMetadataRepository(database)

leetcode_client = LeetCodeClient(
    requests_per_second=1.0,
    leetcode_session=os.getenv(
        "LEETCODE_SESSION"
    ),
    csrf_token=os.getenv(
        "LEETCODE_CSRF_TOKEN"
    ),
)

sync_service = SyncService(
    database=database,
    leetcode_client=leetcode_client,
    user_repository=user_repository,
    problem_repository=problem_repository,
    submission_attempt_repository=submission_attempt_repository,
    submission_repository=submission_repository,
    sync_metadata_repository=sync_metadata_repository,
)


def get_sync_service() -> SyncService:
    return sync_service