from db import (
    Database,
    UserRepository,
    ProblemRecommendationRepository,
)

from problem_recommendation_service import (
    ProblemRecommendationService,
)

from db.recommendation_repository import (
    RecommendationRepository,
)


def main():

    database = Database()

    user_repository = (
        UserRepository(database)
    )

    repository = (
        ProblemRecommendationRepository(
            database
        )
    )

    recommendation_repository = (
        RecommendationRepository(database)
    )

    service = (
        ProblemRecommendationService(
            repository=repository,
            user_repository=user_repository,
            recommendation_repository=recommendation_repository,
        )
    )

    username = "Priyadrasta_Raut"

    topic = "Dynamic Programming"

    # --------------------------------------------------
    # 1. Get initial candidates
    # --------------------------------------------------

    candidates = service.get_candidates(
        username=username,
        topic=topic,
        limit=20,
    )

    print(
        "\n========== INITIAL CANDIDATES =========="
    )

    for candidate in candidates:

        print(
            f"{candidate.problem_id} | "
            f"{candidate.title} | "
            f"{candidate.difficulty} | "
            f"attempts={candidate.previous_attempts}"
        )

    if not candidates:
        print("No candidates found.")
        return

    # --------------------------------------------------
    # 2. Select one candidate to mark as recommended
    # --------------------------------------------------

    selected_candidate = candidates[0]

    print(
        "\n========== MARK AS RECOMMENDED =========="
    )

    print(
        f"Marking: "
        f"{selected_candidate.problem_id} | "
        f"{selected_candidate.title}"
    )

    user = user_repository.find_by_username(
        username
    )

    user_id = user["id"]

    recommendation_repository.save_recommendations(
        user_id=user_id,
        recommendations=[
            {
                "problem_id": selected_candidate.problem_id,
                "topic": topic,
            }
        ],
    )

    # --------------------------------------------------
    # 3. Get candidates again
    # --------------------------------------------------

    filtered_candidates = service.get_candidates(
        username=username,
        topic=topic,
        limit=20,
    )

    print(
        "\n========== FILTERED CANDIDATES =========="
    )

    for candidate in filtered_candidates:

        print(
            f"{candidate.problem_id} | "
            f"{candidate.title} | "
            f"{candidate.difficulty}"
        )

    # --------------------------------------------------
    # 4. Verify selected problem was removed
    # --------------------------------------------------

    filtered_ids = {
        candidate.problem_id
        for candidate in filtered_candidates
    }

    print(
        "\n========== VERIFY FILTERING =========="
    )

    if selected_candidate.problem_id not in filtered_ids:

        print(
            "PASS: Recently recommended problem "
            "was filtered out."
        )

    else:

        print(
            "FAIL: Recently recommended problem "
            "is still present."
        )

    # --------------------------------------------------
    # 5. Verify candidate count
    # --------------------------------------------------

    print(
        f"\nInitial candidate count: "
        f"{len(candidates)}"
    )

    print(
        f"Filtered candidate count: "
        f"{len(filtered_candidates)}"
    )


if __name__ == "__main__":
    main()