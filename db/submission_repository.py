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
        connection: None,
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

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params,
                )

                return cursor.fetchone()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params,
                )

                return cursor.fetchone()

    def exists(
        self,
        submission_id: str,
    ) -> bool:

        query = """
            SELECT EXISTS (
                SELECT 1
                FROM submissions
                WHERE leetcode_submission_id = %s
            ) AS exists;
        """

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (submission_id,),
                )

                result = cursor.fetchone()

                return result["exists"]

    def find_all(self):

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

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(query)

                return cursor.fetchall()

    def count(self) -> int:

        query = """
            SELECT COUNT(*) AS count
            FROM submissions;
        """

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(query)

                result = cursor.fetchone()

                return result["count"]