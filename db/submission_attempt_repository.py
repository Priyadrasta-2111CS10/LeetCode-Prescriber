from typing import Optional

from db.database import Database
from models.submission_attempt import SubmissionAttempt


class SubmissionAttemptRepository:

    def __init__(self, database: Database):
        self.database = database

    def save(
        self,
        attempt: SubmissionAttempt,
        user_id: int,
        problem_id: int,
        connection=None,
    ) -> Optional[dict]:

        query = """
            INSERT INTO submission_attempts (
                leetcode_submission_id,
                user_id,
                problem_id,
                status,
                language,
                runtime,
                memory,
                submitted_at
            )
            VALUES (
                %(leetcode_submission_id)s,
                %(user_id)s,
                %(problem_id)s,
                %(status)s,
                %(language)s,
                %(runtime)s,
                %(memory)s,
                %(submitted_at)s
            )
            ON CONFLICT (leetcode_submission_id)
            DO NOTHING
            RETURNING *;
        """

        params = {
            "leetcode_submission_id":
                attempt.leetcode_submission_id,
            "user_id": user_id,
            "problem_id": problem_id,
            "status": attempt.status,
            "language": attempt.language,
            "runtime": attempt.runtime,
            "memory": attempt.memory,
            "submitted_at": attempt.submitted_at,
        }

        return self.database.execute(
                    query,
                    params,
                    connection=connection,
                    fetch="one",
                )

    def exists_by_leetcode_submission_id(
        self,
        leetcode_submission_id: str,
        connection=None,
    ) -> bool:

        query = """
            SELECT 1
            FROM submission_attempts
            WHERE leetcode_submission_id = %s
            LIMIT 1;
        """

        return (
                self.database.execute(
                    query,
                    (leetcode_submission_id,),
                    connection=connection,
                    fetch="one",
                )
                is not None
            )