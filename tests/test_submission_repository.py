from datetime import datetime, timezone

from db import Database, SubmissionRepository
from models import Submission


def main():

    database = Database()

    repository = SubmissionRepository(
        database
    )

    submission = Submission(
        id="123456789",

        title="Two Sum",

        title_slug="two-sum",

        submitted_at=datetime.now(
            timezone.utc
        ),

        username="test_user",
    )

    result = repository.save(
        submission
    )

    print("\nSubmission saved:")
    print(result)


if __name__ == "__main__":
    main()