import logging


class ProblemEmbeddingService:
    BATCH_SIZE = 50

    def __init__(
        self,
        problem_repository,
        embedding_repository,
        embedding_client,
        embedding_builder,
    ):

        self.problem_repository = (
            problem_repository
        )

        self.embedding_repository = (
            embedding_repository
        )

        self.embedding_client = (
            embedding_client
        )

        self.embedding_builder = (
            embedding_builder
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def embed_problem(
        self,
        problem,
    ):

        content = (
            self.embedding_builder
            .build(problem)
        )

        embedding = (
            self.embedding_client
            .embed(content)
        )

        self.embedding_repository.save(
            problem_id=problem["id"],

            content=content,

            embedding=embedding,

            model=(
                self.embedding_client.MODEL
            ),
        )

    def embed_all(self):

        problems = (
            self.problem_repository
            .find_all()
        )

        pending = []

        skipped = 0

        for problem in problems:

            if (
                self.embedding_repository
                .exists(problem["id"])
            ):

                skipped += 1

                continue

            pending.append(
                problem
            )

        self.logger.info(
            "Total problems=%d, "
            "pending=%d, skipped=%d",
            len(problems),
            len(pending),
            skipped,
        )

        embedded = 0

        failed = 0

        for start in range(
            0,
            len(pending),
            self.BATCH_SIZE,
        ):

            batch = pending[
                start:
                start + self.BATCH_SIZE
            ]

            try:

                contents = [
                    self.embedding_builder.build(
                        problem
                    )
                    for problem in batch
                ]

                self.logger.info(
                    "Embedding batch "
                    "%d-%d",
                    start + 1,
                    start + len(batch),
                )

                embeddings = (
                    self.embedding_client
                    .embed_many(
                        contents
                    )
                )

                if len(embeddings) != len(
                    batch
                ):

                    raise RuntimeError(
                        "Embedding count does "
                        "not match problem count"
                    )

                for problem, embedding in zip(
                    batch,
                    embeddings,
                ):

                    self.embedding_repository.save(
                        problem_id=problem["id"],

                        content=(
                            self.embedding_builder
                            .build(problem)
                        ),

                        embedding=embedding,

                        model=(
                            self.embedding_client
                            .MODEL
                        ),
                    )

                    embedded += 1

            except Exception:

                failed += len(batch)

                self.logger.exception(
                    "Failed embedding batch "
                    "starting at %d",
                    start,
                )

        return {
            "total": len(problems),

            "embedded": embedded,

            "skipped": skipped,

            "failed": failed,
        }