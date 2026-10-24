# import logging
# import time


# class ProblemEmbeddingService:
#     BATCH_SIZE = 90          # stay under the 100/min ceiling with headroom
#     SECONDS_PER_BATCH = 62   # slightly over 60s to be safe against clock drift

#     def __init__(
#         self,
#         problem_repository,
#         embedding_repository,
#         embedding_client,
#         embedding_builder,
#     ):

#         self.problem_repository = (
#             problem_repository
#         )

#         self.embedding_repository = (
#             embedding_repository
#         )

#         self.embedding_client = (
#             embedding_client
#         )

#         self.embedding_builder = (
#             embedding_builder
#         )

#         self.logger = logging.getLogger(
#             self.__class__.__name__
#         )

#     def embed_problem(
#         self,
#         problem,
#     ):

#         content = (
#             self.embedding_builder
#             .build(problem)
#         )

#         embedding = (
#             self.embedding_client
#             .embed(content)
#         )

#         self.embedding_repository.save(
#             problem_id=problem["id"],

#             content=content,

#             embedding=embedding,

#             model=(
#                 self.embedding_client.MODEL
#             ),
#         )

#     def embed_all(self):

#         problems = (
#             self.problem_repository
#             .find_all()
#         )

#         pending = []

#         skipped = 0

#         for problem in problems:

#             if (
#                 self.embedding_repository
#                 .exists(problem["id"])
#             ):

#                 skipped += 1

#                 continue

#             pending.append(
#                 problem
#             )

#         self.logger.info(
#             "Total problems=%d, "
#             "pending=%d, skipped=%d",
#             len(problems),
#             len(pending),
#             skipped,
#         )

#         embedded = 0

#         failed = 0

#         for start in range(
#             0,
#             len(pending),
#             self.BATCH_SIZE,
#         ):

#             batch_start_time = time.monotonic()
#             batch = pending[
#                 start:
#                 start + self.BATCH_SIZE
#             ]

#             try:

#                 contents = [
#                     self.embedding_builder.build(
#                         problem
#                     )
#                     for problem in batch
#                 ]

#                 self.logger.info(
#                     "Embedding batch "
#                     "%d-%d",
#                     start + 1,
#                     start + len(batch),
#                 )

#                 embeddings = (
#                     self.embedding_client
#                     .embed_many(
#                         contents
#                     )
#                 )

#                 if len(embeddings) != len(
#                     batch
#                 ):

#                     raise RuntimeError(
#                         "Embedding count does "
#                         "not match problem count"
#                     )

#                 for problem, content, embedding in zip(
#                     batch,
#                     contents,
#                     embeddings,
#                 ):

#                     self.embedding_repository.save(
#                         problem_id=problem["id"],

#                         content=content,

#                         embedding=embedding,

#                         model=(
#                             self.embedding_client
#                             .MODEL
#                         ),
#                     )

#                     embedded += 1

#             except Exception:

#                 failed += len(batch)

#                 self.logger.exception(
#                     "Failed embedding batch "
#                     "starting at %d",
#                     start,
#                 )

#                 elapsed = time.monotonic() - batch_start_time
#                 if elapsed < self.SECONDS_PER_BATCH:
#                     time.sleep(self.SECONDS_PER_BATCH - elapsed)

#         return {
#             "total": len(problems),

#             "embedded": embedded,

#             "skipped": skipped,

#             "failed": failed,
#         }


import logging
import random
import time

from ai.gemini_embedding_client import DailyQuotaExceededError


class ProblemEmbeddingService:
    BATCH_SIZE = 90          # stay under Gemini's 100/min free-tier cap
    SECONDS_PER_BATCH = 62   # floor per batch; irrelevant once truly local

    # Leaves ~50 units of today's 1000 RPD headroom for live usage
    # (query-time topic embeddings during practice-plan generation share
    # this SAME daily quota bucket) — running the bulk backfill all the
    # way to 1000 would leave zero room to actually test the feature
    # today. Override with a smaller value on days you want even more
    # headroom, or a larger one if you don't need live testing today.
    DEFAULT_MAX_ITEMS_PER_RUN = 700

    def __init__(
        self,
        problem_repository,
        embedding_repository,
        embedding_client,
        embedding_builder,
    ):
        self.problem_repository = problem_repository
        self.embedding_repository = embedding_repository
        self.embedding_client = embedding_client
        self.embedding_builder = embedding_builder
        self.logger = logging.getLogger(self.__class__.__name__)

    def embed_problem(self, problem):
        content = self.embedding_builder.build(problem)
        embedding = self.embedding_client.embed(content)

        self.embedding_repository.save(
            problem_id=problem["id"],
            content=content,
            embedding=embedding,
            model=self.embedding_client.MODEL,
        )

    def embed_all(self, force: bool = False, max_items_per_run: int = None):
        """
        max_items_per_run: caps how many items this call will attempt
        to embed, REGARDLESS of how many are pending. Defaults to
        DEFAULT_MAX_ITEMS_PER_RUN — deliberately below the raw daily
        quota so a bulk backfill run doesn't consume 100% of today's
        budget and starve live usage. Pass None explicitly only if you
        genuinely want to attempt everything pending in one run.
        """

        if max_items_per_run is None:
            max_items_per_run = self.DEFAULT_MAX_ITEMS_PER_RUN

        problems = self.problem_repository.find_all()

        pending = []
        skipped = 0

        for problem in problems:
            if not force and self.embedding_repository.exists(problem["id"]):
                skipped += 1
                continue
            pending.append(problem)

        truncated = False

        if max_items_per_run is not None and len(pending) > max_items_per_run:
            # Shuffle BEFORE truncating — otherwise, across a multi-day
            # partial backfill, you'd systematically embed the catalog's
            # oldest/lowest-numbered problems first (find_all() orders
            # by id), leaving newer problems' topics with zero
            # candidates for days. A random cross-section each run gives
            # much more even topic coverage while the backfill is still
            # incomplete.
            random.shuffle(pending)
            pending = pending[:max_items_per_run]
            truncated = True

        self.logger.info(
            "Total problems=%d, pending=%d (capped_to=%s), skipped=%d, force=%s",
            len(problems), len(pending), max_items_per_run, skipped, force,
        )

        embedded = 0
        failed = 0
        stopped_on_daily_quota = False

        for start in range(0, len(pending), self.BATCH_SIZE):
            batch_start_time = time.monotonic()
            batch = pending[start:start + self.BATCH_SIZE]

            try:
                contents = [
                    self.embedding_builder.build(problem) for problem in batch
                ]

                self.logger.info(
                    "Embedding batch %d-%d", start + 1, start + len(batch)
                )

                embeddings = self.embedding_client.embed_many(contents)

                if len(embeddings) != len(batch):
                    raise RuntimeError(
                        "Embedding count does not match problem count"
                    )

                for problem, content, embedding in zip(batch, contents, embeddings):
                    self.embedding_repository.save(
                        problem_id=problem["id"],
                        content=content,
                        embedding=embedding,
                        model=self.embedding_client.MODEL,
                    )
                    embedded += 1

            except DailyQuotaExceededError:
                # Every remaining batch would fail identically until
                # the quota resets — stop now instead of burning through
                # the rest of `pending` with pointless failed attempts.
                self.logger.error(
                    "Daily quota hit after embedding %d items this run. "
                    "Stopping cleanly — re-run tomorrow (or later) to "
                    "continue; already-embedded problems won't be "
                    "re-processed thanks to the exists() check.",
                    embedded,
                )
                stopped_on_daily_quota = True
                break

            except Exception:
                failed += len(batch)
                self.logger.exception(
                    "Failed embedding batch starting at %d", start
                )

            elapsed = time.monotonic() - batch_start_time
            remaining = self.SECONDS_PER_BATCH - elapsed

            if remaining > 0 and start + self.BATCH_SIZE < len(pending):
                self.logger.info(
                    "Pacing: sleeping %.1fs before next batch", remaining
                )
                time.sleep(remaining)

        return {
            "total": len(problems),
            "embedded": embedded,
            "skipped": skipped,
            "failed": failed,
            "force": force,
            "truncated_to_max_items": truncated,
            "stopped_on_daily_quota": stopped_on_daily_quota,
        }