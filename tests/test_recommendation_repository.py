from db import Database
from db.recommendation_repository import RecommendationRepository
from db.user_repository import UserRepository


def main():

    database = Database()

    user_repository = UserRepository(database)

    recommendation_repository = (
        RecommendationRepository(database)
    )

    # --------------------------------------------------
    # 1. Get existing user
    # --------------------------------------------------

    user = user_repository.find_by_username(
        "Priyadrasta_Raut"
    )

    if user is None:

        print(
            "User not found. Run the real sync first."
        )

        return

    user_id = user["id"]

    print(
        f"Using user: "
        f"{user['username']} "
        f"(id={user_id})"
    )

    # --------------------------------------------------
    # 2. Get recommendations before saving
    # --------------------------------------------------

    print(
        "\n========== GET BEFORE SAVE =========="
    )

    result = (
        recommendation_repository
        .get_recently_recommended_problem_ids(
            user_id
        )
    )

    print(result)

    # --------------------------------------------------
    # 3. Save recommendations
    # --------------------------------------------------

    print(
        "\n========== SAVE RECOMMENDATIONS =========="
    )

    recommendations = [
        {
            "problem_id": 1001,
            "topic": "Rolling Hash",
        },
        {
            "problem_id": 1002,
            "topic": "Dynamic Programming",
        },
        {
            "problem_id": 1003,
            "topic": "Graph Theory",
        },
    ]

    recommendation_repository.save_recommendations(
        user_id=user_id,
        recommendations=recommendations,
    )

    print("Recommendations saved.")

    # --------------------------------------------------
    # 4. Get recommendations after saving
    # --------------------------------------------------

    print(
        "\n========== GET AFTER SAVE =========="
    )

    result = (
        recommendation_repository
        .get_recently_recommended_problem_ids(
            user_id
        )
    )

    print(result)

    # --------------------------------------------------
    # 5. Verify expected problem IDs
    # --------------------------------------------------

    print(
        "\n========== VERIFY PROBLEM IDS =========="
    )

    expected_ids = {
        1001,
        1002,
        1003,
    }

    if expected_ids.issubset(result):

        print(
            "PASS: All recommended problem IDs "
            "were found."
        )

    else:

        print(
            "FAIL: Expected IDs were not found."
        )

        print(
            f"Expected: {expected_ids}"
        )

        print(
            f"Actual: {result}"
        )

    # --------------------------------------------------
    # 6. Verify user isolation
    # --------------------------------------------------

    print(
        "\n========== VERIFY USER ISOLATION =========="
    )

    another_user = (
        user_repository.find_by_username(
            "another_test_user"
        )
    )

    if another_user is not None:

        other_user_result = (
            recommendation_repository
            .get_recently_recommended_problem_ids(
                another_user["id"]
            )
        )

        if expected_ids.isdisjoint(
                other_user_result
        ):

            print(
                "PASS: Recommendations are isolated "
                "between users."
            )

        else:

            print(
                "FAIL: Recommendations leaked "
                "between users."
            )

    else:

        print(
            "SKIPPED: another_test_user does not exist."
        )

    # --------------------------------------------------
    # 7. Verify empty result for unknown user
    # --------------------------------------------------

    print(
        "\n========== VERIFY UNKNOWN USER =========="
    )

    unknown_user_id = -999999

    result = (
        recommendation_repository
        .get_recently_recommended_problem_ids(
            unknown_user_id
        )
    )

    if result == set():

        print(
            "PASS: Unknown user returns empty set."
        )

    else:

        print(
            "FAIL: Expected empty set."
        )

        print(
            f"Actual: {result}"
        )


if __name__ == "__main__":
    main()