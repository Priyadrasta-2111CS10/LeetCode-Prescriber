class AnalyticsRepository:

    def __init__(self, database):

        self.database = database

    def get_overall_stats(
        self,
        user_id: int,
        connection=None,
    ):

        query = """
            SELECT

                COUNT(*) AS total_attempts,

                COUNT(*) FILTER (
                    WHERE status = 'Accepted'
                ) AS accepted_attempts,

                COUNT(*) FILTER (
                    WHERE status <> 'Accepted'
                ) AS rejected_attempts,

                COUNT(
                    DISTINCT problem_id
                ) AS unique_problems_attempted,

                COUNT(
                    DISTINCT problem_id
                ) FILTER (
                    WHERE status = 'Accepted'
                ) AS unique_problems_solved

            FROM submission_attempts

            WHERE user_id = %s;
        """

        return self.database.execute(
                    query,
                    (user_id,),
                    connection=connection,
                    fetch="one",
                )

    def get_difficulty_stats(
        self,
        user_id: int,
        connection=None,
    ):

        query = """
            SELECT

                p.difficulty,

                COUNT(sa.id)
                    AS total_attempts,

                COUNT(sa.id) FILTER (
                    WHERE sa.status = 'Accepted'
                ) AS accepted_attempts,

                COUNT(
                    DISTINCT sa.problem_id
                ) FILTER (
                    WHERE sa.status = 'Accepted'
                ) AS unique_problems_solved

            FROM submission_attempts sa

            JOIN problems p
                ON p.id = sa.problem_id

            WHERE sa.user_id = %s

            GROUP BY p.difficulty

            ORDER BY
                CASE p.difficulty
                    WHEN 'Easy' THEN 1
                    WHEN 'Medium' THEN 2
                    WHEN 'Hard' THEN 3
                    ELSE 4
                END;
        """

        return self.database.execute(
                query,
                (user_id,),
                connection=connection,
                fetch="all",
        )

    def get_topic_stats(
        self,
        user_id: int,
        connection=None,
    ):

        query = """
            SELECT
                topic AS topic,

                COUNT(sa.id) AS total_attempts,

                COUNT(sa.id) FILTER (
                    WHERE sa.status = 'Accepted'
                ) AS accepted_attempts,

                COUNT(
                    DISTINCT sa.problem_id
                ) FILTER (
                    WHERE sa.status = 'Accepted'
                ) AS unique_problems_solved

            FROM submission_attempts sa

            JOIN problems p
                ON p.id = sa.problem_id

            CROSS JOIN LATERAL
                jsonb_array_elements(
                    p.topics
                ) AS topic

            WHERE sa.user_id = %s

            GROUP BY topic

            ORDER BY total_attempts DESC;
        """

        return self.database.execute(
                query,
                (user_id,),
                connection=connection,
                fetch="all",
            )

    def get_status_stats(
        self,
        user_id: int,
        connection=None,
    ):

        query = """
            SELECT
                status,
                COUNT(*) AS count

            FROM submission_attempts

            WHERE user_id = %s

            GROUP BY status

            ORDER BY count DESC;
        """

        return self.database.execute(
                query,
                (user_id,),
                connection=connection,
                fetch="all",
            )