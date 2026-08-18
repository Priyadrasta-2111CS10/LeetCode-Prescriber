from db import Database, ProblemRepository
from models import Problem


def main():

    database = Database()

    repository = ProblemRepository(database)

    problem = Problem(
        question_id="1",
        frontend_id="1",
        title="Two Sum",
        title_slug="two-sum",
        difficulty="Easy",
        topics=[
            "Array",
            "Hash Table",
        ],
        is_paid_only=False,
        acceptance_rate=56.12,
    )

    result = repository.save(problem)

    print("\nProblem saved successfully:")
    print(result)


if __name__ == "__main__":
    main()