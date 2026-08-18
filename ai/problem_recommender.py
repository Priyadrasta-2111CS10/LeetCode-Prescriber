import json

from models import PracticePlan


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

        candidate_data = []

        for candidate in candidates:

            candidate_data.append({

                "problem_id":
                    candidate.problem_id,

                "title":
                    candidate.title,

                "title_slug":
                    candidate.title_slug,

                "difficulty":
                    candidate.difficulty,

                "topics":
                    candidate.topics,

                "previous_attempts":
                    candidate.previous_attempts,

                "previous_accepted_attempts":
                    candidate
                    .previous_accepted_attempts,

                "similarity":
                    round(
                        candidate.similarity,
                        4,
                    ),
            })

        prompt = f"""
You are a coding interview coach.

The user has a weakness in:

Topic:
{topic}

Current acceptance rate:
{acceptance_rate}%

The candidate problems below have already
been retrieved specifically for this user
using:

- topic relevance
- semantic similarity
- previous submission history
- solved/unsolved status

You MUST only recommend problems from
the candidate list.

DO NOT invent problem names.

DO NOT modify titles.

Create a progression of problems that
will help the user improve.

Prefer:

1. Strongly relevant problems.
2. Problems the user has never attempted.
3. Appropriate difficulty progression.
4. Problems that reinforce core patterns.
5. Previously attempted but unsolved
   problems when they are particularly
   valuable.

Candidate problems:

{json.dumps(
    candidate_data,
    indent=2,
    default=str,
)}
"""

        return (
            self.llm_client
            .generate_structured(

                prompt=prompt,

                response_model=(
                    PracticePlan
                ),
            )
        )