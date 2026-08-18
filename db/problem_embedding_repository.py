class ProblemEmbeddingRepository:

    def __init__(
        self,
        database,
    ):

        self.database = database

    def save(
        self,
        problem_id: int,
        content: str,
        embedding: list[float],
        model: str,
        connection=None,
    ):

        query = """
            INSERT INTO problem_embeddings (
                problem_id,
                content,
                embedding,
                model
            )

            VALUES (
                %s,
                %s,
                %s::vector,
                %s
            )

            ON CONFLICT (
                problem_id
            )

            DO UPDATE SET

                content = EXCLUDED.content,

                embedding = EXCLUDED.embedding,

                model = EXCLUDED.model,

                updated_at = NOW();
        """

        vector = (
            "[" +
            ",".join(
                str(value)
                for value in embedding
            ) +
            "]"
        )

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        problem_id,
                        content,
                        vector,
                        model,
                    ),
                )

            return

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        problem_id,
                        content,
                        vector,
                        model,
                    ),
                )

    def exists(
        self,
        problem_id: int,
        connection=None,
    ):

        query = """
            SELECT 1
            FROM problem_embeddings
            WHERE problem_id = %s
            LIMIT 1;
        """

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (problem_id,),
                )

                return cursor.fetchone() is not None

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (problem_id,),
                )

                return cursor.fetchone() is not None