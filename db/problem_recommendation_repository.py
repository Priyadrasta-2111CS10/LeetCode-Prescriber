import json


class ProblemRecommendationRepository:

    def __init__(self, database):

        self.database = database

    def find_candidates(
        self,
        user_id: int,
        topic: str,
        limit: int = 20,
        connection=None,
    ):

        if not topic:
            raise ValueError(
                "topic cannot be empty"
            )

        query = """
            SELECT
                p.id,
                p.title,
                p.title_slug,
                p.difficulty,
                p.topics,

                COUNT(sa.id)
                    AS previous_attempts,

                COUNT(sa.id) FILTER (
                    WHERE sa.status = 'Accepted'
                ) AS previous_accepted_attempts

            FROM problems p

            LEFT JOIN submission_attempts sa
                ON sa.problem_id = p.id
                AND sa.user_id = %s

            WHERE p.topics @> %s::jsonb

            GROUP BY
                p.id,
                p.title,
                p.title_slug,
                p.difficulty,
                p.topics

            ORDER BY

                CASE
                    WHEN COUNT(sa.id) = 0
                        THEN 0
                    ELSE 1
                END,

                CASE p.difficulty
                    WHEN 'Easy' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Hard' THEN 3
                END,

                p.id

            LIMIT %s;
        """

        topic_json = json.dumps(
            [topic]
        )

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        user_id,
                        topic_json,
                        limit,
                    ),
                )

                return cursor.fetchall()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        user_id,
                        topic_json,
                        limit,
                    ),
                )

                return cursor.fetchall()