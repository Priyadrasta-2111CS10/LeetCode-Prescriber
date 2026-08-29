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

        return self.database.execute(
                query,
                (
                    problem_id,
                    content,
                    vector,
                    model,
                ),
                connection=connection,
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

        return (
            self.database.execute(
                query,
                (problem_id,),
                connection=connection,
                fetch="one",
            )
            is not None
        )   