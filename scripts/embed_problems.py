from ai.gemini_embedding_client import GeminiEmbeddingClient
from ai.problem_embedding_builder import ProblemEmbeddingBuilder
from ai.problem_embedding_service import ProblemEmbeddingService
from db import Database, ProblemEmbeddingRepository, ProblemRepository

def main():

    database = Database()

    problem_repository = (
        ProblemRepository(
            database
        )
    )

    embedding_repository = (
        ProblemEmbeddingRepository(
            database
        )
    )

    embedding_client = (
        GeminiEmbeddingClient()
    )

    embedding_builder = (
        ProblemEmbeddingBuilder()
    )

    service = (
        ProblemEmbeddingService(

            problem_repository=(
                problem_repository
            ),

            embedding_repository=(
                embedding_repository
            ),

            embedding_client=(
                embedding_client
            ),

            embedding_builder=(
                embedding_builder
            ),
        )
    )

    result = (
        service.embed_all()
    )

    print(
        "\n========== EMBEDDING RESULT =========="
    )

    print(result)


if __name__ == "__main__":
    main()