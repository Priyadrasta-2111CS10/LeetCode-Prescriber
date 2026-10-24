# from models.ai_problem_recommendation import PracticePlan
# import json


# class AIProblemRecommender:

#     def __init__(
#         self,
#         llm_client,
#     ):
#         self.llm_client = llm_client

#     def recommend(
#         self,
#         topic: str,
#         acceptance_rate: float,
#         candidates,
#     ) -> PracticePlan:

#         candidate_data = []

#         for candidate in candidates:

#             candidate_data.append({
#                 "problem_id": candidate.problem_id,
#                 "title": candidate.title,
#                 "title_slug": candidate.title_slug,
#                 "difficulty": candidate.difficulty,
#                 "topics": candidate.topics,
#                 "previous_attempts": (
#                     candidate.previous_attempts
#                 ),
#                 "previous_accepted_attempts": (
#                     candidate.previous_accepted_attempts
#                 ),
#                 "similarity": round(
#                     candidate.similarity,
#                     4,
#                 ),
#             })

#         prompt = f"""
# You are a coding interview coach.

# ...

# Candidate problems:

# {json.dumps(
#     candidate_data,
#     indent=2,
#     default=str,
# )}
# """

#         return self.llm_client.generate_structured(
#             prompt=prompt,
#             response_model=PracticePlan,
#         )

#     def get_recommended_problem_ids(
#         self,
#         plan: PracticePlan,
#         candidates,
#     ) -> list[int]:

#         candidate_ids_by_title = {
#             candidate.title: candidate.problem_id
#             for candidate in candidates
#         }

#         recommended_ids = []

#         for problem in plan.problems:

#             problem_id = candidate_ids_by_title.get(
#                 problem.title
#             )

#             if problem_id is not None:
#                 recommended_ids.append(
#                     problem_id
#                 )

#         return recommended_ids

import json

from models.ai_problem_recommendation import PracticePlan, PracticePlanBatch


class AIProblemRecommender:

    def __init__(
        self,
        llm_client,
    ):
        self.llm_client = llm_client

    def recommend(
        self,
        topic: str,
        acceptance_rate: float,
        candidates,
    ) -> PracticePlan:
        """
        Single-topic version — kept for cases where you genuinely only
        need one plan (e.g. a "regenerate just this topic" button).
        For a full practice-plan generation across several weak topics,
        use recommend_batch() instead — it costs one LLM call total
        rather than one per topic.
        """

        candidate_data = self._serialize_candidates(candidates)

        prompt = f"""
You are a coding interview coach.

The user has a weakness in:

Topic:
{topic}

Current acceptance rate:
{acceptance_rate}%

The candidate problems below have already been retrieved specifically
for this user using topic relevance, semantic similarity, previous
submission history, and solved/unsolved status.

You MUST only recommend problems from the candidate list. DO NOT invent
problem names. DO NOT modify titles.

Create a progression of problems that will help the user improve.

Candidate problems:

{json.dumps(candidate_data, indent=2, default=str)}
"""

        return self.llm_client.generate_structured(
            prompt=prompt,
            response_model=PracticePlan,
        )

    def recommend_batch(
        self,
        topics: list[dict],
    ) -> PracticePlanBatch:
        """
        topics: list of {"topic": str, "acceptance_rate": float,
                          "candidates": list[ProblemCandidate]}

        Builds one prompt covering every topic and its own candidate
        list, and asks for one PracticePlan per topic back in a single
        structured response — this is what actually collapses N Gemini
        calls (one per weak topic) down to 1 call per generate_plan()
        invocation.
        """

        if not topics:
            raise ValueError("topics cannot be empty")

        topic_blocks = []

        for entry in topics:
            candidate_data = self._serialize_candidates(entry["candidates"])

            topic_blocks.append({
                "topic": entry["topic"],
                "acceptance_rate": entry["acceptance_rate"],
                "candidates": candidate_data,
            })

        prompt = f"""
You are a coding interview coach building a practice plan that covers
SEVERAL weak topics at once for the same user.

You are given a list of topics below. Each topic has its own
"acceptance_rate" (the user's current weakness on that topic) and its
own "candidates" list (problems already retrieved specifically for
that topic using relevance, similarity, and submission history).

Rules — these apply to EVERY topic independently:
- Return exactly one plan per topic, in the same order as given below.
- Each plan's "topic" field MUST exactly match the topic string given
  for it below — do not paraphrase or reformat it.
- Only recommend problems from that topic's OWN candidate list. DO NOT
  borrow a problem from a different topic's candidate list. DO NOT
  invent problem titles. DO NOT modify titles.
- Create a sensible difficulty/priority progression within each topic's
  plan, same as you would for a single-topic request.

Topics and their candidate problems:

{json.dumps(topic_blocks, indent=2, default=str)}
"""

        return self.llm_client.generate_structured(
            prompt=prompt,
            response_model=PracticePlanBatch,
        )

    def get_recommended_problem_ids(
        self,
        plan: PracticePlan,
        candidates,
    ) -> list[int]:

        candidate_ids_by_title = {
            candidate.title: candidate.problem_id
            for candidate in candidates
        }

        recommended_ids = []

        for problem in plan.problems:

            problem_id = candidate_ids_by_title.get(problem.title)

            if problem_id is not None:
                recommended_ids.append(problem_id)

        return recommended_ids

    @staticmethod
    def _serialize_candidates(candidates) -> list[dict]:

        return [
            {
                "problem_id": candidate.problem_id,
                "title": candidate.title,
                "title_slug": candidate.title_slug,
                "difficulty": candidate.difficulty,
                "topics": candidate.topics,
                "previous_attempts": candidate.previous_attempts,
                "previous_accepted_attempts": candidate.previous_accepted_attempts,
                "similarity": round(candidate.similarity, 4),
            }
            for candidate in candidates
        ]