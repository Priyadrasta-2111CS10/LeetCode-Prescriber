from typing import Any, Dict


class AISnapshotBuilder:

    MAX_TOPICS = 10

    def build(
        self,
        snapshot,
    ) -> Dict[str, Any]:

        topics = sorted(
            snapshot.topics,
            key=lambda x: (
                x["acceptance_rate"]
            ),
        )

        weak_topics = topics[
            :self.MAX_TOPICS
        ]

        difficulty = snapshot.difficulty

        return {
            "username": snapshot.username,

            "overall": snapshot.overall,

            "difficulty": difficulty,

            "weak_topics": weak_topics,

            "submission_status":
                snapshot.submission_status,
        }