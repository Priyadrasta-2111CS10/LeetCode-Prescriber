# import logging

# from ai.gemini_embedding_client import GeminiEmbeddingClient
# from ai.problem_embedding_builder import ProblemEmbeddingBuilder
# from ai.problem_embedding_service import ProblemEmbeddingService
# from db import Database, ProblemRepository
# from db.problem_embedding_repository import ProblemEmbeddingRepository
# from leetcode_client import LeetCodeClient
# from models import Problem

# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger("sync_problem_catalog")


# def main():
#     database = Database()
#     problem_repository = ProblemRepository(database)
#     embedding_repository = ProblemEmbeddingRepository(database)
#     embedding_client = GeminiEmbeddingClient()
#     embedding_builder = ProblemEmbeddingBuilder()
#     client = LeetCodeClient(requests_per_second=1.0)

#     saved = 0
#     failed = 0

#     try:
#         for question in client.iter_all_problems(page_size=100):

#             topic_names = [
#                 tag["name"] for tag in question.get("topicTags", [])
#             ]

#             frontend_id = question["frontendQuestionId"]

#             problem = Problem(
#                 question_id=frontend_id,   # see note below
#                 frontend_id=frontend_id,
#                 title=question["title"],
#                 title_slug=question["titleSlug"],
#                 difficulty=question["difficulty"],
#                 topics=topic_names,
#                 is_paid_only=question["paidOnly"],
#                 acceptance_rate=question.get("acRate"),
#             )

#             try:
#                 problem_repository.save(problem)
#                 saved += 1
#             except Exception:
#                 logger.exception(
#                     "Failed to save problem %s", question["titleSlug"]
#                 )
#                 failed += 1

#             if saved % 200 == 0:
#                 logger.info("Progress: saved=%d failed=%d", saved, failed)

#     finally:
#         client.close()

#     logger.info("Done. saved=%d failed=%d", saved, failed)

#     # Embed anything new
#     embedding_service = ProblemEmbeddingService(
#         problem_repository=problem_repository,
#         embedding_repository=embedding_repository,
#         embedding_client=embedding_client,
#         embedding_builder=embedding_builder,
#     )

#     embedding_result = embedding_service.embed_all()
#     logger.info("Embedding sync: %s", embedding_result)


# if __name__ == "__main__":
#     main()


import argparse
import logging
import time

import psycopg
from ai.gemini_embedding_client import GeminiEmbeddingClient
from ai.problem_embedding_builder import ProblemEmbeddingBuilder
from ai.problem_embedding_service import ProblemEmbeddingService
from db import Database, ProblemRepository
from db.problem_embedding_repository import ProblemEmbeddingRepository
from leetcode_client import LeetCodeClient
from models import Problem

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("sync_problem_catalog")

DATABASE_RETRIES = 3


def sync_problems(problem_repository, client) -> dict:

    saved = 0
    failed = 0
    connection = None

    try:
        for question in client.iter_all_problems(page_size=100):

            # topicTags is LeetCode's own official API response — the exact
            # same tag list rendered on the problem's real page on
            # leetcode.com. This IS the source of truth; nothing further
            # to validate it against. (An earlier version of this script
            # cross-checked tags against a third-party reference list and
            # rejected anything not on it — that was a mistake: it flagged
            # genuinely official tags, like "Sqrt Decomposition" on Range
            # Sum Query - Mutable, as if they were corrupted data. Trust
            # this field directly.)
            topic_names = [tag["name"] for tag in question.get("topicTags", [])]

            frontend_id = question["frontendQuestionId"]

            problem = Problem(
                question_id=frontend_id,
                frontend_id=frontend_id,
                title=question["title"],
                title_slug=question["titleSlug"],
                difficulty=question["difficulty"],
                topics=topic_names,
                is_paid_only=question["paidOnly"],
                acceptance_rate=question.get("acRate"),
            )

            try:
                for attempt in range(DATABASE_RETRIES):
                    try:
                        if connection is None or connection.closed:
                            connection = problem_repository.database.get_connection()

                        with connection.transaction():
                            problem_repository.save(problem, connection=connection)
                        saved += 1
                        break
                    except psycopg.OperationalError:
                        if connection is not None:
                            connection.close()
                            connection = None
                        if attempt == DATABASE_RETRIES - 1:
                            raise
                        delay = 2 ** attempt
                        logger.warning(
                            "Database connection failed for %s; retrying in %d "
                            "second(s) (%d/%d)",
                            question["titleSlug"],
                            delay,
                            attempt + 1,
                            DATABASE_RETRIES - 1,
                        )
                        time.sleep(delay)
            except Exception:
                logger.exception("Failed to save problem %s", question["titleSlug"])
                failed += 1

            if saved and saved % 200 == 0:
                logger.info("Progress: saved=%d failed=%d", saved, failed)
    finally:
        if connection is not None:
            connection.close()

    return {"saved": saved, "failed": failed}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--force-reembed",
        action="store_true",
        help=(
            "Rebuild EVERY problem's embedding, not just new ones. "
            "Use this after a bulk data correction so stale embeddings "
            "can't silently disagree with corrected topics."
        ),
    )
    args = parser.parse_args()

    database = Database()
    problem_repository = ProblemRepository(database)
    embedding_repository = ProblemEmbeddingRepository(database)
    embedding_client = GeminiEmbeddingClient()
    embedding_builder = ProblemEmbeddingBuilder()
    client = LeetCodeClient(requests_per_second=1.0)

    try:
        sync_result = sync_problems(problem_repository, client)
    finally:
        client.close()

    logger.info("Problem sync done: %s", sync_result)

    embedding_service = ProblemEmbeddingService(
        problem_repository=problem_repository,
        embedding_repository=embedding_repository,
        embedding_client=embedding_client,
        embedding_builder=embedding_builder,
    )

    embedding_result = embedding_service.embed_all(force=args.force_reembed)
    logger.info("Embedding sync: %s", embedding_result)


if __name__ == "__main__":
    main()