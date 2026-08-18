from ai.gemini_embedding_client import GeminiEmbeddingClient
from ai.gemini_client import GeminiClient
from ai.personalized_retrieval_service import PersonalizedRetrievalService
from ai.problem_recommender import AIProblemRecommender
from analytics.weakness_detector import WeaknessDetector
from analytics_service import AnalyticsService
from db import Database, ProblemEmbeddingSearchRepository, UserRepository, AnalyticsRepository
from practice_plan_service import PracticePlanService


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

    search_repository = (
        ProblemEmbeddingSearchRepository(
            database
        )
    )

    embedding_client = (
        GeminiEmbeddingClient()
    )

    retrieval_service = (
        PersonalizedRetrievalService(

            user_repository=(
                user_repository
            ),

            search_repository=(
                search_repository
            ),

            embedding_client=(
                embedding_client
            ),
        )
    )

    llm_client = GeminiClient()

    ai_problem_recommender = (
        AIProblemRecommender(
            llm_client=llm_client
        )
    )

    practice_plan_service = (
        PracticePlanService(

            analytics_service=(
                analytics_service
            ),

            retrieval_service=(
                retrieval_service
            ),

            ai_problem_recommender=(
                ai_problem_recommender
            ),
        )
    )

    username = "Priyadrasta_Raut"

    plans = (
        practice_plan_service
        .generate_plan(
            username=username,

            candidates_per_topic=20,
        )
    )

    print(
        "\n========== PRACTICE PLANS =========="
    )

    for plan in plans:

        print(
            f"\nTOPIC: {plan.topic}"
        )

        print(
            f"GOAL: {plan.goal}"
        )

        for problem in plan.problems:

            print(
                f"{problem.suggested_order}. "
                f"{problem.title} | "
                f"{problem.priority}"
            )

            print(
                f"   {problem.reason}"
            )


if __name__ == "__main__":
    main()