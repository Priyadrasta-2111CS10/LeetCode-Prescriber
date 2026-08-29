import logging
from datetime import datetime, timedelta, timezone
import uuid

from db import Database


class RecommendationRepository:

    def __init__(self, database: Database):
        self.database = database
        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def get_recently_recommended_problem_ids(
            self,
            user_id: int,
            days: int = 30,
            connection=None,
    ) -> set[int]:

        cutoff = (
            datetime.now(timezone.utc)
            - timedelta(days=days)
        )
        rows = self.database.execute(
            """
            SELECT problem_id
            FROM recommendation_history
            WHERE user_id = %s
              AND recommended_at >= %s
            """,
            (
                user_id,
                cutoff,
            ),
            connection=connection,
            fetch="all",
        )

        return {
            row["problem_id"]
            for row in rows
        
        }

    def save_recommendations(
        self,
        user_id: int,
        recommendations: list[dict],
        connection=None,
) -> None:

        if not recommendations:
            return

        plan_id = uuid.uuid4()
        recommended_at = datetime.now(timezone.utc)

        for recommendation in recommendations:

            self.database.execute(
                """
                INSERT INTO recommendation_history (
                    user_id,
                    problem_id,
                    topic,
                    recommended_at,
                    plan_id
                )
                VALUES (
                    %s,
                    %s,
                    %s,
                    %s,
                    %s
                )
                """,
                (
                    user_id,
                    recommendation["problem_id"],
                    recommendation["topic"],
                    recommended_at,
                    plan_id,
                ),
                connection=connection,
            )