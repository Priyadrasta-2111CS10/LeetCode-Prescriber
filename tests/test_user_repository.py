from db import Database, UserRepository
from models import User


def main():

    database = Database()

    repository = UserRepository(database)

    user = User(
        username="test_user",
        ranking=12345,
        real_name="Test User",
        country_name="India",
        company="Test Company",
        job_title="Software Engineer",
        websites=[],
        skill_tags=[],
    )

    result = repository.save(user)

    print("\nUser saved successfully:")
    print(result)


if __name__ == "__main__":
    main()