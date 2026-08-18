import os
from datetime import datetime, timezone

from db import (
    Database,
    ProblemRepository,
    SubmissionAttemptRepository,
    UserRepository,
)

from dotenv import load_dotenv

from leetcode_client import LeetCodeClient
from models import SubmissionAttempt,  Problem


load_dotenv()


def main():

    database = Database()

    user_repository = UserRepository(
        database
    )

    problem_repository = ProblemRepository(
        database
    )

    attempt_repository = (
        SubmissionAttemptRepository(
            database
        )
    )

    # -----------------------------------------
    # Get the real user
    # -----------------------------------------

    user = user_repository.find_by_username(
        "Priyadrasta_Raut"
    )

    if user is None:

        raise RuntimeError(
            "User does not exist. "
            "Run the normal sync first."
        )

    user_id = user["id"]

    # -----------------------------------------
    # Create authenticated client
    # -----------------------------------------

    client = LeetCodeClient(
        requests_per_second=1.0,
        leetcode_session=os.getenv(
            "LEETCODE_SESSION"
        ),
        csrf_token=os.getenv(
            "LEETCODE_CSRF_TOKEN"
        ),
    )

    try:

        # -------------------------------------
        # Fetch 30 submission attempts
        # -------------------------------------

        submissions = []

        for raw in client.iter_submission_history(
            page_size=10
        ):

            submissions.append(raw)

            if len(submissions) >= 30:
                break

        print(
            f"Fetched {len(submissions)} "
            "submission attempts"
        )

        inserted = 0
        existing = 0
        missing_problems = 0

        # -------------------------------------
        # Process submissions
        # -------------------------------------

        for raw in submissions:

            title_slug = raw["titleSlug"]

            # ---------------------------------
            # Find problem
            # ---------------------------------

            problem = (
                problem_repository.find_by_slug(
                    title_slug
                )
            )

            if problem is None:

                print(
                    f"Problem not found locally. "
                    f"Fetching: {title_slug}"
                )

                raw_problem = client.get_problem(
                    title_slug
                )

                problem = Problem(
                    question_id=str(
                        raw_problem["questionId"]
                    ),

                    frontend_id=str(
                        raw_problem["questionFrontendId"]
                    ),

                    title=raw_problem["title"],

                    title_slug=raw_problem["titleSlug"],

                    difficulty=raw_problem["difficulty"],

                    topics=[
                        tag["name"]
                        for tag in raw_problem["topicTags"]
                    ],

                    is_paid_only=raw_problem["isPaidOnly"],

                    acceptance_rate=raw_problem["acRate"],
                )

                problem = problem_repository.save(
                    problem
                )

            # ---------------------------------
            # Build SubmissionAttempt
            # ---------------------------------

            attempt = SubmissionAttempt(

                leetcode_submission_id=
                    str(raw["id"]),

                username=user["username"],

                title=raw["title"],

                title_slug=title_slug,

                status=raw["statusDisplay"],

                language=raw.get("lang"),

                runtime=raw.get("runtime"),

                memory=raw.get("memory"),

                submitted_at=
                    datetime.fromtimestamp(
                        int(raw["timestamp"]),
                        tz=timezone.utc,
                    ),
            )

            # ---------------------------------
            # Save attempt
            # ---------------------------------

            result = attempt_repository.save(
                attempt=attempt,
                user_id=user_id,
                problem_id=problem["id"],
            )

            if result is None:

                existing += 1

            else:

                inserted += 1

        # -------------------------------------
        # Result
        # -------------------------------------

        print(
            "\n========== RESULT =========="
        )

        print(
            "Fetched:",
            len(submissions),
        )

        print(
            "Inserted:",
            inserted,
        )

        print(
            "Existing:",
            existing,
        )

        print(
            "Missing problems:",
            missing_problems,
        )

    finally:

        client.close()


if __name__ == "__main__":
    main()