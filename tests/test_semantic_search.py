from ai.gemini_embedding_client import GeminiEmbeddingClient
from ai.problem_semantic_search_service import ProblemSemanticSearchService
from db import Database, ProblemEmbeddingSearchRepository


def main():

    database = Database()

    search_repository = (
        ProblemEmbeddingSearchRepository(
            database
        )
    )

    embedding_client = (
        GeminiEmbeddingClient()
    )

    service = (
        ProblemSemanticSearchService(

            embedding_client=(
                embedding_client
            ),

            search_repository=(
                search_repository
            ),
        )
    )

    query = """
    I want to practice dynamic programming
    problems involving one dimensional state,
    recurrence relations, and choosing between
    different states.
    """

    results = service.search(
        query=query,
        limit=10,
    )

    print(
        "\n========== SEMANTIC SEARCH =========="
    )

    for row in results:

        print(
            f"{row['title']} | "
            f"{row['difficulty']} | "
            f"similarity="
            f"{row['similarity']:.4f}"
        )


if __name__ == "__main__":
    main()