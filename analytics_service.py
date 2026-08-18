import logging

from models import DifficultyStats, OverallStats, TopicStats, AnalyticsSnapshot



class AnalyticsService:

    def __init__(
        self,
        analytics_repository,
        user_repository,
        weakness_detector,
    ):

        self.analytics_repository = (
            analytics_repository
        )

        self.user_repository = (
            user_repository
        )

        self.weakness_detector = (
            weakness_detector
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def get_overall_stats(
        self,
        username: str,
    ) -> OverallStats:

        user = (
            self.user_repository.find_by_username(
                username
            )
        )

        if user is None:

            raise ValueError(
                f"User '{username}' not found"
            )

        raw = (
            self.analytics_repository
            .get_overall_stats(
                user["id"]
            )
        )

        total_attempts = (
            raw["total_attempts"]
            or 0
        )

        accepted_attempts = (
            raw["accepted_attempts"]
            or 0
        )

        rejected_attempts = (
            raw["rejected_attempts"]
            or 0
        )

        unique_problems_attempted = (
            raw[
                "unique_problems_attempted"
            ]
            or 0
        )

        unique_problems_solved = (
            raw[
                "unique_problems_solved"
            ]
            or 0
        )

        acceptance_rate = 0.0

        if total_attempts > 0:

            acceptance_rate = (
                accepted_attempts
                / total_attempts
            ) * 100

        return OverallStats(

            total_attempts=total_attempts,

            accepted_attempts=(
                accepted_attempts
            ),

            rejected_attempts=(
                rejected_attempts
            ),

            unique_problems_attempted=(
                unique_problems_attempted
            ),

            unique_problems_solved=(
                unique_problems_solved
            ),

            acceptance_rate=round(
                acceptance_rate,
                2,
            ),
        )

    def get_difficulty_stats(
        self,
        username: str,
    ):

        user = (
            self.user_repository.find_by_username(
                username
            )
        )

        if user is None:

            raise ValueError(
                f"User '{username}' not found"
            )

        rows = (
            self.analytics_repository
            .get_difficulty_stats(
                user["id"]
            )
        )

        result = []

        for row in rows:

            total_attempts = (
                row["total_attempts"]
                or 0
            )

            accepted_attempts = (
                row["accepted_attempts"]
                or 0
            )

            acceptance_rate = 0.0

            if total_attempts > 0:

                acceptance_rate = (
                    accepted_attempts
                    / total_attempts
                ) * 100

            result.append(
                DifficultyStats(

                    difficulty=row[
                        "difficulty"
                    ],

                    total_attempts=(
                        total_attempts
                    ),

                    accepted_attempts=(
                        accepted_attempts
                    ),

                    unique_problems_solved=(
                        row[
                            "unique_problems_solved"
                        ]
                        or 0
                    ),

                    acceptance_rate=round(
                        acceptance_rate,
                        2,
                    ),
                )
            )

        return result

    def get_topic_stats(
        self,
        username: str,
    ):

        user = (
            self.user_repository.find_by_username(
                username
            )
        )

        if user is None:

            raise ValueError(
                f"User '{username}' not found"
            )

        rows = (
            self.analytics_repository
            .get_topic_stats(
                user["id"]
            )
        )

        result = []

        for row in rows:

            total_attempts = (
                row["total_attempts"]
                or 0
            )

            accepted_attempts = (
                row["accepted_attempts"]
                or 0
            )

            acceptance_rate = 0.0

            if total_attempts > 0:

                acceptance_rate = (
                    accepted_attempts
                    / total_attempts
                ) * 100

            result.append(
                TopicStats(

                    topic=row["topic"],

                    total_attempts=(
                        total_attempts
                    ),

                    accepted_attempts=(
                        accepted_attempts
                    ),

                    unique_problems_solved=(
                        row[
                            "unique_problems_solved"
                        ]
                        or 0
                    ),

                    acceptance_rate=round(
                        acceptance_rate,
                        2,
                    ),
                )
            )

        return result


    def get_weak_topics(
        self,
        username: str,
    ):

        topic_stats = (
            self.get_topic_stats(
                username
            )
        )

        return self.weakness_detector.detect(
            topic_stats
        )


    def get_status_stats(
        self,
        username: str,
    ):

        user = (
            self.user_repository.find_by_username(
                username
            )
        )

        if user is None:

            raise ValueError(
                f"User '{username}' not found"
            )

        return (
            self.analytics_repository
            .get_status_stats(
                user["id"]
            )
        )



    def build_snapshot(
        self,
        username: str,
    ) -> AnalyticsSnapshot:

        overall = (
            self.get_overall_stats(
                username
            )
        )

        difficulty = (
            self.get_difficulty_stats(
                username
            )
        )

        topics = (
            self.get_topic_stats(
                username
            )
        )

        weak_topics = (
            self.get_weak_topics(
                username
            )
        )

        submission_status = (
            self.get_status_stats(
                username
            )
        )

        # -----------------------------------------
        # Convert dataclasses to dictionaries
        # -----------------------------------------

        overall_data = {
            "total_attempts":
                overall.total_attempts,

            "accepted_attempts":
                overall.accepted_attempts,

            "rejected_attempts":
                overall.rejected_attempts,

            "unique_problems_attempted":
                overall.unique_problems_attempted,

            "unique_problems_solved":
                overall.unique_problems_solved,

            "acceptance_rate":
                overall.acceptance_rate,
        }

        difficulty_data = []

        for stats in difficulty:

            difficulty_data.append({
                "difficulty":
                    stats.difficulty,

                "total_attempts":
                    stats.total_attempts,

                "accepted_attempts":
                    stats.accepted_attempts,

                "unique_problems_solved":
                    stats.unique_problems_solved,

                "acceptance_rate":
                    stats.acceptance_rate,
            })

        topic_data = []

        for stats in topics:

            topic_data.append({
                "topic":
                    stats.topic,

                "total_attempts":
                    stats.total_attempts,

                "accepted_attempts":
                    stats.accepted_attempts,

                "unique_problems_solved":
                    stats.unique_problems_solved,

                "acceptance_rate":
                    stats.acceptance_rate,
            })

        weak_topic_data = []

        for stats in weak_topics:

            weak_topic_data.append({
                "topic":
                    stats.topic,

                "total_attempts":
                    stats.total_attempts,

                "accepted_attempts":
                    stats.accepted_attempts,

                "unique_problems_solved":
                    stats.unique_problems_solved,

                "acceptance_rate":
                    stats.acceptance_rate,
            })

        status_data = []

        for row in submission_status:

            status_data.append({
                "status":
                    row["status"],

                "count":
                    row["count"],
            })

        return AnalyticsSnapshot(

            username=username,

            overall=overall_data,

            difficulty=difficulty_data,

            topics=topic_data,

            weak_topics=weak_topic_data,

            submission_status=status_data,
        )