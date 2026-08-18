from db import (
    Database,
    UserRepository,
    ProblemRecommendationRepository,
)

from problem_recommendation_service import (
    ProblemRecommendationService,
)


def main():

    database = Database()

    user_repository = (
        UserRepository(
            database
        )
    )

    repository = (
        ProblemRecommendationRepository(
            database
        )
    )

    service = (
        ProblemRecommendationService(
            repository=repository,
            user_repository=user_repository,
        )
    )

    username = "Priyadrasta_Raut"

    topic = "Dynamic Programming"

    candidates = (
        service.get_candidates(
            username=username,
            topic=topic,
            limit=20,
        )
    )

    print(
        "\n========== CANDIDATES =========="
    )

    for candidate in candidates:

        print(
            f"{candidate.title} | "
            f"{candidate.difficulty} | "
            f"attempts="
            f"{candidate.previous_attempts}"
        )


if __name__ == "__main__":
    main()