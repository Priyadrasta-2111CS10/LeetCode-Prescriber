import json


class ProblemEmbeddingBuilder:

    def build(
        self,
        problem,
    ) -> str:

        topics = problem["topics"]

        if isinstance(
            topics,
            str,
        ):

            topics = json.loads(
                topics
            )

        topic_text = ", ".join(
            topics
        )

        return f"""
LeetCode Problem

Title:
{problem["title"]}

Difficulty:
{problem["difficulty"]}

Topics:
{topic_text}
""".strip()