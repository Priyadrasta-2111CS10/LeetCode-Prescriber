from models import ProblemCandidate


class ProblemRecommendationService:

    def __init__(
        self,
        repository,
        user_repository,
    ):

        self.repository = repository

        self.user_repository = (
            user_repository
        )

    def get_candidates(
        self,
        username: str,
        topic: str,
        limit: int = 20,
    ):

        user = (
            self.user_repository
            .find_by_username(
                username
            )
        )

        if user is None:

            raise ValueError(
                f"User '{username}' not found"
            )

        rows = (
            self.repository
            .find_candidates(
                user_id=user["id"],
                topic=topic,
                limit=limit,
            )
        )

        result = []

        for row in rows:

            result.append(
                ProblemCandidate(

                    problem_id=row["id"],

                    title=row["title"],

                    title_slug=row[
                        "title_slug"
                    ],

                    difficulty=row[
                        "difficulty"
                    ],

                    topics=row["topics"],

                    previous_attempts=(
                        row[
                            "previous_attempts"
                        ]
                        or 0
                    ),

                    previous_accepted_attempts=(
                        row[
                            "previous_accepted_attempts"
                        ]
                        or 0
                    ),
                )
            )

        return result