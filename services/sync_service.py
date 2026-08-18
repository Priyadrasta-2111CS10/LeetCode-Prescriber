# import json
import logging
from datetime import datetime, timezone
from typing import Any, Dict

from db import Database
from leetcode_client import LeetCodeClient
from models import Problem, Submission, SubmissionAttempt, User, SyncCursor
from repository import (ProblemRepository, SubmissionAttemptRepository,
                        SubmissionRepository, SyncMetadataRepository,
                        UserRepository)

from config import (
    LEETCODE_INITIAL_SYNC_LIMIT,
    LEETCODE_SUBMISSION_PAGE_SIZE,
)


class SyncService:

    def __init__(
        self,
        leetcode_client: LeetCodeClient,
        user_repository: UserRepository,
        problem_repository: ProblemRepository,
        submission_repository: SubmissionRepository,
        submission_attempt_repository : SubmissionAttemptRepository,
        sync_metadata_repository : SyncMetadataRepository,
        database : Database,
    ):

        self.leetcode_client = leetcode_client
        self.user_repository = user_repository
        self.problem_repository = problem_repository
        self.submission_repository = submission_repository
        self.submission_attempt_repository = submission_attempt_repository
        self.sync_metadata_repository = sync_metadata_repository
        self.database = database
        self.submission_page_size = (
            LEETCODE_SUBMISSION_PAGE_SIZE
        )

        self.initial_sync_limit = (
            LEETCODE_INITIAL_SYNC_LIMIT
        )
        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def sync_user(
        self,
        username: str,
    ) -> Dict[str, Any]:

        self.logger.info(
            "Starting synchronization for user=%s",
            username,
        )

        # =====================================================
        # 1. Fetch user/profile data from LeetCode
        # =====================================================

        data = self.leetcode_client.get_user_data(
            username
        )

        user = self._build_user(
            username,
            data["profile"],
        )

        # =====================================================
        # 2. Save / update user
        # =====================================================

        user_record = self.user_repository.save(
            user
        )

        user_id = user_record["id"]

        # =====================================================
        # 3. Get previous sync metadata
        # =====================================================
        sync_metadata = (
            self.sync_metadata_repository
            .get_by_user_id(user_id)
        )

        cursor = self._build_sync_cursor(
            sync_metadata
        )

        self.logger.info(
            "Synchronization cursor: "
            "submission_id=%s, timestamp=%s",
            cursor.submission_id,
            cursor.submission_timestamp,
        )

        # self.logger.info(
        #     "Last synchronized submission=%s",
        #     latest_submission,
        # )

        # =====================================================
        # 4. Fetch new submissions
        #
        # No database transaction is open here.
        # =====================================================

        submissions = self._fetch_submissions_for_sync(cursor)
    


        self.logger.info(
            "Fetched %d new submission attempts",
            len(submissions),
        )

        # =====================================================
        # 5. Mark sync as RUNNING
        #
        # Use a separate connection so RUNNING survives a
        # later transaction rollback.
        # =====================================================

        try:

            with self.database.get_connection() as connection:

                self.sync_metadata_repository.start_sync(
                    user_id=user_id,
                    connection=connection,
                )

        except Exception:

            self.logger.exception(
                "Failed to mark sync as RUNNING "
                "for user=%s",
                username,
            )

            raise

        new_attempts = 0
        existing_attempts = 0
        new_solved_problems = 0

        # =====================================================
        # 6. Main database transaction
        # =====================================================

        try:

            with self.database.get_connection() as connection:

                # =============================================
                # Process every submission attempt
                # =============================================

                for raw_submission in submissions:

                    attempt = (
                        self._build_submission_attempt(
                            raw_submission,
                            username,
                        )
                    )

                    # -----------------------------------------
                    # Get or create problem
                    # -----------------------------------------

                    problem = (
                        self._get_or_create_problem(
                            attempt.title_slug,
                            connection=connection,
                        )
                    )

                    # -----------------------------------------
                    # Save every submission attempt
                    # -----------------------------------------

                    attempt_result = (
                        self.submission_attempt_repository.save(
                            attempt=attempt,
                            user_id=user_id,
                            problem_id=problem["id"],
                            connection=connection,
                        )
                    )

                    if attempt_result is None:

                        existing_attempts += 1

                    else:

                        new_attempts += 1

                    # -----------------------------------------
                    # Save accepted submission
                    # -----------------------------------------

                    if attempt.status == "Accepted":

                        submission = (
                            self._build_submission(
                                raw_submission,
                                username,
                            )
                        )

                        solved_result = (
                            self.submission_repository.save(
                                submission=submission,
                                connection=connection,
                            )
                        )

                        if solved_result is not None:

                            new_solved_problems += 1

                # =============================================
                # 7. Determine latest processed submission
                # =============================================

                latest_submission = None

                if submissions:

                    latest_submission = self._get_latest_submission(submissions)

                # =============================================
                # 8. Complete sync
                # =============================================

                self.sync_metadata_repository.complete_sync(
                    user_id=user_id,

                    submission_id=(
                        str(
                            latest_submission["id"]
                        )
                        if latest_submission
                        else cursor.submission_id
                    ),

                    submission_timestamp=(
                        datetime.fromtimestamp(
                            int(
                                latest_submission[
                                    "timestamp"
                                ]
                            ),
                            tz=timezone.utc,
                        )
                        if latest_submission
                        else cursor.submission_timestamp
                    ),

                    connection=connection,
                )

        # =====================================================
        # 9. Handle failure
        # =====================================================

        except Exception as exc:

            self.logger.exception(
            "Synchronization failed for user=%s",
            username,
        )

            try:

                with self.database.get_connection() as connection:

                    self.sync_metadata_repository.fail_sync(
                        user_id=user_id,
                        error=str(exc),
                        connection=connection,
                    )

            except Exception:

                self.logger.exception(
                    "Failed to mark synchronization "
                    "as FAILED",
                )

            raise

        # =====================================================
        # 10. Return result
        # =====================================================

        result = {
            "username": username,

            "new_attempts":
                new_attempts,

            "existing_attempts":
                existing_attempts,

            "new_solved_problems":
                new_solved_problems,

            "total_attempts_processed":
                len(submissions),
        }

        self.logger.info(
            "Synchronization completed: %s",
            result,
        )

        return result
                


    # =====================================================
    # Mapping methods
    # =====================================================

    def _build_user(
        self,
        username: str,
        profile: Dict[str, Any],
    ) -> User:

        profile_data = profile.get(
            "profile",
            {}
        )

        return User(
            username=username,

            ranking=profile_data.get(
                "ranking"
            ),

            real_name=profile_data.get(
                "realName"
            ),

            about_me=profile_data.get(
                "aboutMe"
            ),

            school=profile_data.get(
                "school"
            ),

            country_name=profile_data.get(
                "countryName"
            ),

            company=profile_data.get(
                "company"
            ),

            job_title=profile_data.get(
                "jobTitle"
            ),

            github_url=profile.get(
                "githubUrl"
            ),

            twitter_url=profile.get(
                "twitterUrl"
            ),

            linkedin_url=profile.get(
                "linkedinUrl"
            ),

            avatar_url=profile_data.get(
                "userAvatar"
            ),

            websites=profile_data.get(
                "websites"
            ),

            skill_tags=profile_data.get(
                "skillTags"
            ),

            reputation=profile_data.get(
                "reputation"
            ),

            solution_count=profile_data.get(
                "solutionCount"
            ),

            category_discuss_count=profile_data.get(
                "categoryDiscussCount"
            ),
        )

    def _build_submission(
        self,
        raw_submission,
        username,
        ) -> Submission:

        return Submission(
            id=str(
                raw_submission["id"]
            ),

            title=raw_submission["title"],

            title_slug=raw_submission["titleSlug"],

            submitted_at=datetime.fromtimestamp(
                int(raw_submission["timestamp"]),
                tz=timezone.utc,
            ),

            username=username,
        )

    def _build_problem(
        self,
        data: Dict[str, Any],
    ) -> Problem:

        self.logger.debug(
            "Problem metadata: title=%s, acRate=%s",
            data.get("title"),
            data.get("acRate"),
        )

        topics = [
            tag["name"]
            for tag in data.get(
                "topicTags",
                []
            )
        ]

        acceptance_rate = data.get(
            "acRate"
        )

        if acceptance_rate is not None:
            acceptance_rate = float(
                acceptance_rate
            )

        return Problem(
            question_id=str(
                data["questionId"]
            ),

            frontend_id=str(
                data["questionFrontendId"]
            ),

            title=data["title"],

            title_slug=data["titleSlug"],

            difficulty=data["difficulty"],

            topics=topics,

            is_paid_only=data.get(
                "isPaidOnly",
                False
            ),

            acceptance_rate=acceptance_rate,
        )


    def _sync_problem(
        self,
        title_slug: str,
    ) -> Problem:

        existing_problem = (
            self.problem_repository.find_by_slug(
                title_slug
            )
        )

        if existing_problem is not None:

            self.logger.debug(
                "Problem already exists: %s",
                title_slug,
            )

            return existing_problem

        self.logger.info(
            "Fetching problem metadata: %s",
            title_slug,
        )

        raw_problem = (
            self.leetcode_client.get_problem(
                title_slug
            )
        )

        problem = self._build_problem(
            raw_problem
        )

        self.problem_repository.save(
            problem
        )

        return problem


    def _build_submission_attempt(
        self,
        raw_submission,
        username,
    ) -> SubmissionAttempt:

        return SubmissionAttempt(
            leetcode_submission_id=str(
                raw_submission["id"]
            ),

            username= username,

            title=raw_submission["title"],

            title_slug=raw_submission["titleSlug"],

            status=raw_submission["statusDisplay"],

            language=raw_submission.get("lang"),

            runtime=raw_submission.get("runtime"),

            memory=raw_submission.get("memory"),

            submitted_at=datetime.fromtimestamp(
                int(raw_submission["timestamp"]),
                tz=timezone.utc,
            ),
        )

    def _get_or_create_problem(
            self,
            title_slug,
            connection=None,
        ):

        problem = (
            self.problem_repository.find_by_slug(
                title_slug,
                connection=connection,
            )
        )

        if problem is not None:

            return problem

        self.logger.info(
            "Problem not found locally. "
            "Fetching from LeetCode: %s",
            title_slug,
        )

        raw_problem = (
            self.leetcode_client.get_problem(
                title_slug
            )
        )

        problem = Problem(

            question_id=str(
                raw_problem["questionId"]
            ),

            frontend_id=str(
                raw_problem[
                    "questionFrontendId"
                ]
            ),

            title=raw_problem["title"],

            title_slug=raw_problem[
                "titleSlug"
            ],

            difficulty=raw_problem[
                "difficulty"
            ],

            topics=[
                tag["name"]
                for tag
                in raw_problem["topicTags"]
            ],

            is_paid_only=raw_problem[
                "isPaidOnly"
            ],

            acceptance_rate=raw_problem[
                "acRate"
            ],
        )

        return self.problem_repository.save(
            problem,
            connection=connection,
        )

    def get_by_user_id(
        self,
        user_id: int,
        connection=None,
    ):
        query = """
            SELECT *
            FROM sync_metadata
            WHERE user_id = %s;
        """

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (user_id,),
                )

                return cursor.fetchone()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (user_id,),
                )

                return cursor.fetchone()

    def _fetch_submissions_for_sync(
        self,
        cursor: SyncCursor,
    ) -> list[dict]:

        submissions = []

        page_size = (
            self.submission_page_size
        )

        initial_sync_limit = (
            self.initial_sync_limit
        )

        for raw_submission in (
            self.leetcode_client
            .iter_submission_history(
                page_size=page_size
            )
        ):

            submission_id = str(
                raw_submission["id"]
            )

            submission_timestamp = (
                datetime.fromtimestamp(
                    int(
                        raw_submission[
                            "timestamp"
                        ]
                    ),
                    tz=timezone.utc,
                )
            )

            # =================================================
            # Existing synchronization cursor
            # =================================================

            if cursor.exists:

                # ---------------------------------------------
                # Exact submission already synchronized
                # ---------------------------------------------

                if (
                    submission_id
                    == cursor.submission_id
                ):

                    self.logger.info(
                        "Reached synchronization "
                        "cursor: submission_id=%s",
                        submission_id,
                    )

                    break

                # ---------------------------------------------
                # Safety check:
                # If the API somehow returns an older
                # submission after the cursor timestamp,
                # don't process it as new.
                # ---------------------------------------------

                if (
                    cursor.submission_timestamp
                    is not None
                    and submission_timestamp
                    <= cursor.submission_timestamp
                ):

                    self.logger.debug(
                        "Skipping submission=%s "
                        "because timestamp=%s is not "
                        "newer than cursor timestamp=%s",
                        submission_id,
                        submission_timestamp,
                        cursor.submission_timestamp,
                    )

                    continue

            # =================================================
            # New submission
            # =================================================

            submissions.append(
                raw_submission
            )

            # =================================================
            # Initial sync safety limit
            # =================================================

            if (
                not cursor.exists
                and len(submissions)
                >= initial_sync_limit
            ):

                self.logger.info(
                    "Reached initial synchronization "
                    "limit=%d",
                    initial_sync_limit,
                )

                break

        return submissions

    def _build_sync_cursor(
        self,
        sync_metadata,
    ) -> SyncCursor:

        if sync_metadata is None:

            return SyncCursor()

        return SyncCursor(
            submission_id=(
                str(
                    sync_metadata[
                        "last_submission_id"
                    ]
                )
                if sync_metadata[
                    "last_submission_id"
                ] is not None
                else None
            ),

            submission_timestamp=(
                sync_metadata[
                    "last_submission_timestamp"
                ]
            ),
        )


    def _get_latest_submission(
        self,
        submissions,
    ):

        if not submissions:
            return None

        return max(
            submissions,
            key=lambda submission: (
                int(
                    submission["timestamp"]
                ),
                int(
                    submission["id"]
                ),
            ),
        )