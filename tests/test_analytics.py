import json

from analytics.weakness_detector import WeaknessDetector
from analytics_service import AnalyticsService
from db import AnalyticsRepository, Database, UserRepository


def main():

    database = Database()

    user_repository = (
        UserRepository(
            database
        )
    )

    analytics_repository = (
        AnalyticsRepository(
            database
        )
    )

    analytics_service = (
        AnalyticsService(
            analytics_repository=(
                analytics_repository
            ),

            user_repository=(
                user_repository
            ),

            weakness_detector = WeaknessDetector()
        )
    )

    username = "Priyadrasta_Raut"

    # print(
    #     "\n========== OVERALL =========="
    # )

    # overall = (
    #     analytics_service
    #     .get_overall_stats(
    #         username
    #     )
    # )

    # print(overall)

    # print(
    #     "\n========== DIFFICULTY =========="
    # )

    # difficulty = (
    #     analytics_service
    #     .get_difficulty_stats(
    #         username
    #     )
    # )

    # for stats in difficulty:

    #     print(stats)

    # print("\n========== TOPICS ==========")

    # topics = (
    #     analytics_service
    #     .get_topic_stats(
    #         username
    #     )
    # )

    # for stats in topics:

    #     print(stats)

    # print(
    # "\n========== WEAK TOPICS =========="
    # )

    # weak_topics = (
    #     analytics_service
    #     .get_weak_topics(
    #         username
    #     )
    # )

    # for topic in weak_topics:

    #     print(
    #         f"{topic.topic}: "
    #         f"{topic.acceptance_rate}%"
    #     )

    # print(
    #     "\n========== SUBMISSION STATUS =========="
    # )

    # statuses = (
    #     analytics_service
    #     .get_status_stats(
    #         username
    #     )
    # )

    # for row in statuses:

    #     print(
    #         row["status"],
    #         row["count"],
    #     )


    print(
    "\n========== ANALYTICS SNAPSHOT =========="
    )

    snapshot = (
        analytics_service
        .build_snapshot(
            username
        )
    )

    print(
    json.dumps(
        snapshot.__dict__,
        indent=4,
        default=str,
    )
)

if __name__ == "__main__":
    main()