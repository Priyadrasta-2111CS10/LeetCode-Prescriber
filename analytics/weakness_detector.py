from models import TopicStats


class WeaknessDetector:

    def __init__(
        self,
        minimum_attempts: int = 5,
        acceptance_threshold: float = 50.0,
    ):

        self.minimum_attempts = (
            minimum_attempts
        )

        self.acceptance_threshold = (
            acceptance_threshold
        )


    def detect(
        self,
        topic_stats: list[TopicStats],
    ) -> list[TopicStats]:

        weak_topics = []

        for stats in topic_stats:

            if (
                stats.total_attempts
                < self.minimum_attempts
            ):
                continue

            if (
                stats.acceptance_rate
                < self.acceptance_threshold
            ):

                weak_topics.append(
                    stats
                )

        weak_topics.sort(
            key=lambda x:
                x.acceptance_rate
        )

        return weak_topics