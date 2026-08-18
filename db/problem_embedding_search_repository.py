import json


class ProblemEmbeddingSearchRepository:

    def __init__(
        self,
        database,
    ):

        self.database = database

    def search_personalized(
        self,
        user_id: int,
        topic: str,
        query_embedding: list[float],
        limit: int = 20,
        connection=None,
    ):

        query = """
            WITH user_problem_stats AS (

                SELECT
                    problem_id,

                    COUNT(*) AS total_attempts,

                    COUNT(*) FILTER (
                        WHERE status = 'Accepted'
                    ) AS accepted_attempts,

                    MAX(submitted_at)
                        AS last_attempted_at

                FROM submission_attempts

                WHERE user_id = %s

                GROUP BY problem_id
            )

            SELECT

                p.id AS problem_id,

                p.title,

                p.title_slug,

                p.difficulty,

                p.topics,

                COALESCE(
                    ups.total_attempts,
                    0
                ) AS previous_attempts,

                COALESCE(
                    ups.accepted_attempts,
                    0
                ) AS previous_accepted_attempts,

                ups.last_attempted_at,

                1 - (
                    pe.embedding
                    <=> %s::vector
                ) AS similarity

            FROM problem_embeddings pe

            JOIN problems p
                ON p.id = pe.problem_id

            LEFT JOIN user_problem_stats ups
                ON ups.problem_id = p.id

            WHERE
                p.topics ? %s

                AND COALESCE(
                    ups.accepted_attempts,
                    0
                ) = 0

            ORDER BY

                (
                    1 - (
                        pe.embedding
                        <=> %s::vector
                    )
                ) DESC,

                CASE
                    WHEN COALESCE(
                        ups.total_attempts,
                        0
                    ) = 0
                    THEN 0
                    ELSE 1
                END,

                COALESCE(
                    ups.total_attempts,
                    0
                ) ASC

            LIMIT %s;
        """

        vector = (
            "["
            + ",".join(
                str(value)
                for value in query_embedding
            )
            + "]"
        )

        params = (
            user_id,
            vector,
            topic,
            vector,
            limit,
        )

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params,
                )

                return cursor.fetchall()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params,
                )

                return cursor.fetchall()