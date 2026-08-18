import logging, os

from dotenv import load_dotenv
from leetcode_client import LeetCodeClient

from db import (
    Database,
    UserRepository,
    ProblemRepository,
    SubmissionRepository,
    SubmissionAttemptRepository,
    SyncMetadataRepository,
)
load_dotenv()
from services.sync_service import SyncService


logging.basicConfig(
    level=logging.INFO,
    format=(
        "%(asctime)s | "
        "%(levelname)s | "
        "%(name)s | "
        "%(message)s"
    ),
)


def main():

    # username = input(
    #     "Enter LeetCode username: "
    # ).strip()
    username = "Priyadrasta_Raut"

    client = LeetCodeClient(
        requests_per_second=1.0,
        leetcode_session=os.getenv(
        "LEETCODE_SESSION"
    ),

    csrf_token=os.getenv(
        "LEETCODE_CSRF_TOKEN"
    ),
    )


    database = Database()
    user_repository = UserRepository(database)
    problem_repository = ProblemRepository(database)
    submission_repository = SubmissionRepository(database)
    submission_attempt_repository = SubmissionAttemptRepository(database)
    sync_metadata_repository = SyncMetadataRepository(database)

    sync_service = SyncService (
        leetcode_client = client,
        user_repository = user_repository,
        problem_repository = problem_repository,
        submission_repository = submission_repository,
        submission_attempt_repository = submission_attempt_repository,
        sync_metadata_repository = sync_metadata_repository,
        database = database,
    )

    try:

        result = sync_service.sync_user(
            username
        )

        print(
            "\n========== SYNC RESULT =========="
        )

        print(result)

        print(
            "\nStored submissions:",
            submission_repository.count()
        )

    finally:

        client.close()


if __name__ == "__main__":
    main()