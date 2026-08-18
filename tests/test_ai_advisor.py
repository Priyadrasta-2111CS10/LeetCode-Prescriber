import json

from ai.gemini_client import GeminiClient
from ai.practice_advisor import AIPracticeAdvisor
from analytics.weakness_detector import WeaknessDetector
from analytics_service import AnalyticsService
from db import AnalyticsRepository, Database, UserRepository
from ai.ai_snapshot import AISnapshotBuilder

import os

from dotenv import load_dotenv

load_dotenv()

# print(
#     "OLLAMA_BASE_URL:",
#     os.getenv("OLLAMA_BASE_URL")
# )

# print(
#     "OLLAMA_MODEL:",
#     os.getenv("OLLAMA_MODEL")
# )

# print(
#     "OLLAMA_TIMEOUT:",
#     os.getenv("OLLAMA_TIMEOUT")
# )

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

            weakness_detector=(
                WeaknessDetector()
            ),
        )
    )

    username = (
        "Priyadrasta_Raut"
    )

    # =============================================
    # Build deterministic analytics
    # =============================================

    snapshot = (
        analytics_service
        .build_snapshot(
            username
        )
    )

    # print(
    #     "\n========== SNAPSHOT =========="
    # )

    # print(
    #     json.dumps(
    #         snapshot.__dict__,
    #         indent=2,
    #         default=str,
    #     )
    # )

    # =============================================
    # AI
    # =============================================


    gemini_client = GeminiClient()

    advisor = (
    AIPracticeAdvisor(

        llm_client= gemini_client,

        snapshot_builder=(
            AISnapshotBuilder()
        ),
    )
)

    # try:

    analysis = (
        advisor.analyze(
            snapshot
        )
    )

    print(
        "\n========== AI ANALYSIS =========="
    )

    print(
        "Summary:"
    )

    print(
        analysis.summary
    )

    print(
        "\nStrengths:"
    )

    for strength in (
        analysis.strengths
    ):

        print(
            f"- {strength}"
        )

    print(
        "\nWeaknesses:"
    )

    for weakness in (
        analysis.weaknesses
    ):

        print(
            f"- {weakness}"
        )

    print(
        "\nRecommendations:"
    )

    for recommendation in (
        analysis.recommendations
    ):

        print(
            f"- [{recommendation.priority}] "
            f"{recommendation.topic}"
        )

        print(
            f"  {recommendation.reason}"
        )

    # finally:

    #     ollama_client.close()


if __name__ == "__main__":
    main()