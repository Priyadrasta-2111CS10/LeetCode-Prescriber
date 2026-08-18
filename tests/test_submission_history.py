import os

from dotenv import load_dotenv

from leetcode_client import LeetCodeClient


load_dotenv()


def main():

    client = LeetCodeClient(
        requests_per_second=1.0,

        leetcode_session=os.getenv(
            "LEETCODE_SESSION"
        ),

        csrf_token=os.getenv(
            "LEETCODE_CSRF_TOKEN"
        ),
    )

    try:

        result = client.get_submission_history(
            limit=10,
            offset=0,
        )

        print(result)

    finally:

        client.close()


if __name__ == "__main__":
    main()