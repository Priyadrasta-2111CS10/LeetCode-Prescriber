from typing import Optional

from db.database import Database
from models import Submission


class SubmissionRepository:

    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def save(
        self,
        submission: Submission,
        connection = None,
    ) -> dict:

        query = """
            INSERT INTO submissions (
                leetcode_submission_id,
                user_id,
                problem_id,
                submitted_at
            )
            SELECT
                %s,
                u.id,
                p.id,
                %s
            FROM users u
            CROSS JOIN problems p
            WHERE u.username = %s
              AND p.title_slug = %s
            ON CONFLICT (
                leetcode_submission_id
            )
            DO NOTHING
            RETURNING *;
        """

        params = (
            submission.id,
            submission.submitted_at,
            submission.username,
            submission.title_slug,
        )

        return self.database.execute(
                query,
                params,
                connection=connection,
                fetch="one",
            )

    def exists(
        self,
        submission_id: str,
        connection = None,
    ) -> bool:

        query = """
            SELECT EXISTS (
                SELECT 1
                FROM submissions
                WHERE leetcode_submission_id = %s
            ) AS exists;
        """

        result = self.database.execute(
                query,
                (submission_id,),
                connection=connection,
                fetch="one",
            )

        return result["exists"]

    def find_all(self,
        connection=None,):

        query = """
            SELECT
                s.id,
                s.leetcode_submission_id,
                u.username,
                p.title,
                p.title_slug,
                p.difficulty,
                s.submitted_at
            FROM submissions s
            JOIN users u
                ON s.user_id = u.id
            JOIN problems p
                ON s.problem_id = p.id
            ORDER BY s.submitted_at DESC;
        """

        return self.database.execute(
                query,
                connection=connection,
                fetch="all",
            )

    def count(self,
              connection=None,
              ) -> int:

        query = """
            SELECT COUNT(*) AS count
            FROM submissions;
        """

        result =  self.database.execute(
                        query,
                        connection=connection,
                        fetch="one",
                    )

        return result["count"]