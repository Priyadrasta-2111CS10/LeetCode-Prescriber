class PracticePlanService:

    def __init__(
        self,
        analytics_service,
        retrieval_service,
        ai_problem_recommender,
    ):

        self.analytics_service = (
            analytics_service
        )

        self.retrieval_service = (
            retrieval_service
        )

        self.ai_problem_recommender = (
            ai_problem_recommender
        )

    def generate_plan(
        self,
        username: str,
        candidates_per_topic: int = 20,
    ):

        weak_topics = (
            self.analytics_service
            .get_weak_topics(
                username
            )
        )

        plans = []

        for weak_topic in weak_topics:

            candidates = (
                self.retrieval_service
                .retrieve(

                    username=username,

                    topic=weak_topic.topic,

                    acceptance_rate=(
                        weak_topic
                        .acceptance_rate
                    ),

                    limit=(
                        candidates_per_topic
                    ),
                )
            )

            if not candidates:

                continue

            plan = (
                self.ai_problem_recommender
                .recommend(

                    topic=(
                        weak_topic.topic
                    ),

                    acceptance_rate=(
                        weak_topic
                        .acceptance_rate
                    ),

                    candidates=candidates,
                )
            )

            plans.append(plan)

        return plans