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

        print("========== AUTH STATUS ==========")

        status = client.get_user_status()

        print(status)

        print(
            "\n========== FETCH USER DATA =========="
        )

        data = client.get_user_data(
            "Priyadrasta_Raut"
        )

        print(
            "User data fetched successfully"
        )

        print(
            "\n========== FETCH HISTORY =========="
        )

        result = client.get_submission_history(
            limit=20,
            offset=0,
        )

        print(
            "Submission count:",
            len(
                result.get("submissions", [])
            )
        )

        print(
            "hasNext:",
            result.get("hasNext")
        )

    finally:

        client.close()


if __name__ == "__main__":
    main()