import json
import logging

from models import (AnalyticsSnapshot, PracticeRecommendation,
                    TopicRecommendation)


class AIPracticeAdvisor:

    def __init__(
        self,
        llm_client,
        snapshot_builder,
    ):

        # self.ollama_client = (
        #     ollama_client
        # )

        self.llm_client = llm_client

        self.snapshot_builder = (
            snapshot_builder
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def analyze(
        self,
        snapshot: AnalyticsSnapshot,
    ) -> PracticeRecommendation:

        prompt = (
            self._build_prompt(
                snapshot
            )
        )

        return (
            self.llm_client
            .generate_structured(

                prompt=prompt,

                response_model=(
                    PracticeRecommendation
                ),
            )
        )
    
    def _build_prompt(
        self,
        snapshot: AnalyticsSnapshot,
    ) -> str:

        ai_snapshot = (
            self.snapshot_builder.build(
                snapshot
            )
        )

        snapshot_json = json.dumps(
            ai_snapshot,
            indent=2,
        )

        return f"""
    You are a coding interview coach analyzing
    a user's LeetCode practice history.

    Analyze the supplied statistics and identify:

    1. The user's strongest areas.
    2. The user's weakest areas.
    3. Important failure patterns.
    4. Topics they should practice next.
    5. Why those topics deserve priority.

    Rules:

    - Use only the supplied statistics.
    - Do not invent statistics or problems.
    - Do not assume skills that are not represented
    in the data.
    - Give HIGH priority only when there is
    sufficient evidence of weakness.
    - Recommendations should be actionable for
    software engineering interview preparation.

    LeetCode analytics:

    {snapshot_json}
    """

    # def _parse_response(
    #     self,
    #     raw_response: str,
    # ) -> PracticeRecommendation:

    #     try:

    #         data = json.loads(
    #             raw_response
    #         )

    #     except json.JSONDecodeError as exc:

    #         self.logger.error(
    #             "Ollama returned invalid JSON: %s",
    #             raw_response,
    #         )

    #         raise ValueError(
    #             "Ollama returned invalid JSON"
    #         ) from exc

    #     summary = data.get(
    #         "summary"
    #     )

    #     strengths = data.get(
    #         "strengths",
    #         [],
    #     )

    #     weaknesses = data.get(
    #         "weaknesses",
    #         [],
    #     )

    #     recommendations = data.get(
    #         "recommendations",
    #         [],
    #     )

    #     if not isinstance(
    #         summary,
    #         str,
    #     ):

    #         raise ValueError(
    #             "Invalid AI response: "
    #             "'summary' must be a string"
    #         )

    #     if not isinstance(
    #         strengths,
    #         list,
    #     ):

    #         raise ValueError(
    #             "Invalid AI response: "
    #             "'strengths' must be a list"
    #         )

    #     if not isinstance(
    #         weaknesses,
    #         list,
    #     ):

    #         raise ValueError(
    #             "Invalid AI response: "
    #             "'weaknesses' must be a list"
    #         )

    #     parsed_recommendations = []

    #     for recommendation in recommendations:

    #         if not isinstance(
    #             recommendation,
    #             dict,
    #         ):

    #             continue

    #         topic = recommendation.get(
    #             "topic"
    #         )

    #         reason = recommendation.get(
    #             "reason"
    #         )

    #         priority = recommendation.get(
    #             "priority",
    #             "MEDIUM",
    #         )

    #         if not topic or not reason:

    #             continue

    #         parsed_recommendations.append(
    #             TopicRecommendation(
    #                 topic=topic,
    #                 reason=reason,
    #                 priority=priority,
    #             )
    #         )

    #     return PracticeRecommendation(

    #         summary=summary,

    #         strengths=strengths,

    #         weaknesses=weaknesses,

    #         recommendations=(
    #             parsed_recommendations
    #         ),
    #     )