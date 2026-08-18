from typing import Optional

from db.database import Database
from models import Problem
from psycopg.types.json import Jsonb


class ProblemRepository:

    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def save(self, problem: Problem, connection=None,) -> dict:

        query = """
            INSERT INTO problems (
                question_id,
                frontend_id,
                title,
                title_slug,
                difficulty,
                topics,
                is_paid_only,
                acceptance_rate
            )
            VALUES (
                %(question_id)s,
                %(frontend_id)s,
                %(title)s,
                %(title_slug)s,
                %(difficulty)s,
                %(topics)s,
                %(is_paid_only)s,
                %(acceptance_rate)s
            )
            ON CONFLICT (title_slug)
            DO UPDATE SET
                question_id = EXCLUDED.question_id,
                frontend_id = EXCLUDED.frontend_id,
                title = EXCLUDED.title,
                difficulty = EXCLUDED.difficulty,
                topics = EXCLUDED.topics,
                is_paid_only = EXCLUDED.is_paid_only,
                acceptance_rate =
                    EXCLUDED.acceptance_rate,
                updated_at = NOW()
            RETURNING *;
        """

        params = {
            "question_id": problem.question_id,
            "frontend_id": problem.frontend_id,
            "title": problem.title,
            "title_slug": problem.title_slug,
            "difficulty": problem.difficulty,
            "topics": Jsonb(
                problem.topics
            ),
            "is_paid_only": problem.is_paid_only,
            "acceptance_rate":
                problem.acceptance_rate,
        }

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

    def find_by_slug(
        self,
        title_slug: str,
        connection = None,
    ) -> Optional[dict]:

        query = """
            SELECT *
            FROM problems
            WHERE title_slug = %s;
        """
        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (title_slug,),
                )

                return cursor.fetchone()
            
        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (title_slug,),
                )

                return cursor.fetchone()

    def find_all(
        self,
        connection=None,
    ):
        query = """
            SELECT
                id,
                question_id,
                frontend_id,
                title,
                title_slug,
                difficulty,
                topics,
                is_paid_only,
                acceptance_rate
            FROM problems
            ORDER BY id;
        """

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(query)

                return cursor.fetchall()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(query)

                return cursor.fetchall()