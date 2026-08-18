from models import ProblemCandidate


class PersonalizedRetrievalService:

    def __init__(
        self,
        user_repository,
        search_repository,
        embedding_client,
    ):

        self.user_repository = (
            user_repository
        )

        self.search_repository = (
            search_repository
        )

        self.embedding_client = (
            embedding_client
        )

    def retrieve(
        self,
        username: str,
        topic: str,
        acceptance_rate: float,
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

        query = self._build_query(
            topic=topic,
            acceptance_rate=(
                acceptance_rate
            ),
        )

        query_embedding = (
            self.embedding_client
            .embed(query)
        )

        rows = (
            self.search_repository
            .search_personalized(

                user_id=user["id"],

                topic=topic,

                query_embedding=(
                    query_embedding
                ),

                limit=limit,
            )
        )

        return [
            self._to_candidate(row)
            for row in rows
        ]

    @staticmethod
    def _build_query(
        topic: str,
        acceptance_rate: float,
    ) -> str:

        return f"""
        LeetCode interview practice.

        Weak topic:
        {topic}

        Current acceptance rate:
        {acceptance_rate}%

        Focus on problems involving:
        - {topic}
        - core patterns of {topic}
        - interview-oriented applications
        - appropriate problem-solving techniques

        Find problems that help improve
        this weakness.
        """.strip()

    @staticmethod
    def _to_candidate(
        row,
    ) -> ProblemCandidate:

        return ProblemCandidate(

            problem_id=row[
                "problem_id"
            ],

            title=row[
                "title"
            ],

            title_slug=row[
                "title_slug"
            ],

            difficulty=row[
                "difficulty"
            ],

            topics=row[
                "topics"
            ],

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

            similarity=float(
                row[
                    "similarity"
                ]
            ),

            last_attempted_at=row[
                "last_attempted_at"
            ],
        )

# Notice that we're making **only one embedding request per weak topic**.

# If the user has:

# ```text
# 5 weak topics