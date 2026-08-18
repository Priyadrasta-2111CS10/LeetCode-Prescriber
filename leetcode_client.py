import logging
import time
from typing import Any, Dict, List, Optional

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


class LeetCodeClientError(Exception):
    """Base exception for LeetCode client errors."""


class LeetCodeNetworkError(LeetCodeClientError):
    """Raised when a network-level error occurs."""


class LeetCodeAPIError(LeetCodeClientError):
    """Raised when LeetCode returns a GraphQL/API error."""


class LeetCodeResponseError(LeetCodeClientError):
    """Raised when LeetCode returns an unexpected response."""


class RateLimiter:
    """
    Simple client-side rate limiter.

    Ensures that we don't make requests more frequently
    than requests_per_second.
    """

    def __init__(self, requests_per_second: float = 1.0):
        if requests_per_second <= 0:
            raise ValueError("requests_per_second must be greater than 0")

        self.min_interval = 1.0 / requests_per_second
        self.last_request_time = 0.0

    def wait(self) -> None:
        elapsed = time.monotonic() - self.last_request_time

        if elapsed < self.min_interval:
            time.sleep(self.min_interval - elapsed)

        self.last_request_time = time.monotonic()


class LeetCodeClient:

    BASE_URL = "https://leetcode.com/graphql"

    DEFAULT_TIMEOUT = (5, 15)  # connection timeout, read timeout

    def __init__(
        self,
        timeout=None,
        requests_per_second: float = 1.0,
        leetcode_session: str | None = None,
        csrf_token: str | None = None,
    ):
        self.timeout = timeout or self.DEFAULT_TIMEOUT

        self.logger = logging.getLogger(self.__class__.__name__)

        self.session = requests.Session()

        self.session.headers.update({
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 "
                "Safari/537.36"
            ),
            "Content-Type": "application/json",
            "Referer": "https://leetcode.com/",
        })

        if leetcode_session:

            self.session.cookies.set(
                "LEETCODE_SESSION",
                leetcode_session,
                domain=".leetcode.com",
            )

        if csrf_token:

            self.session.cookies.set(
                "csrftoken",
                csrf_token,
                domain=".leetcode.com",
            )

            self.session.headers.update({
                "x-csrftoken": csrf_token,
            })


        self.rate_limiter = RateLimiter(
            requests_per_second=requests_per_second
        )

    # =========================================================
    # Session / HTTP Configuration
    # =========================================================

    def _create_session(self) -> requests.Session:

        session = requests.Session()

        retry_strategy = Retry(
            total=3,

            # Retry these HTTP status codes
            status_forcelist=[
                429,  # Too Many Requests
                500,
                502,
                503,
                504,
            ],

            # Retry on these HTTP methods
            allowed_methods=[
                "POST",
            ],

            # Exponential backoff:
            # 0s, 1s, 2s, 4s...
            backoff_factor=1,

            # Respect Retry-After header when provided
            respect_retry_after_header=True,
        )

        adapter = HTTPAdapter(
            max_retries=retry_strategy,
            pool_connections=10,
            pool_maxsize=10,
        )

        session.mount("https://", adapter)
        session.mount("http://", adapter)

        session.headers.update({
            "Content-Type": "application/json",
            "Accept": "application/json",
            "User-Agent": (
                "Mozilla/5.0 "
                "(Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 "
                "(KHTML, like Gecko) "
                "Chrome/151.0.0.0 Safari/537.36"
            ),
        })

        return session

    # =========================================================
    # Generic GraphQL Request
    # =========================================================

    def _query(
        self,
        query: str,
        variables: Optional[Dict[str, Any]] = None,
        operation_name: Optional[str] = None,
    ) -> Dict[str, Any]:

        payload = {
            "query": query,
            "variables": variables or {},
        }

        if operation_name:
            payload["operationName"] = operation_name

        self.rate_limiter.wait()

        self.logger.debug(
            "Sending GraphQL request: operation=%s",
            operation_name,
        )

        try:

            response = self.session.post(
                self.BASE_URL,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.exceptions.Timeout as exc:

            self.logger.error(
                "Request timed out: operation=%s",
                operation_name,
            )

            raise LeetCodeNetworkError(
                "Request to LeetCode timed out"
            ) from exc

        except requests.exceptions.ConnectionError as exc:

            self.logger.error(
                "Connection error: operation=%s",
                operation_name,
            )

            raise LeetCodeNetworkError(
                "Could not connect to LeetCode"
            ) from exc

        except requests.exceptions.HTTPError as exc:

            self.logger.error(
                "HTTP error: status=%s operation=%s",
                response.status_code,
                operation_name,
            )

            raise LeetCodeAPIError(
                f"LeetCode returned HTTP {response.status_code}"
            ) from exc

        except requests.exceptions.RequestException as exc:

            self.logger.error(
                "Unexpected request error: operation=%s",
                operation_name,
            )

            raise LeetCodeNetworkError(
                "Unexpected network error while contacting LeetCode"
            ) from exc

        # -----------------------------------------------------
        # Validate JSON
        # -----------------------------------------------------

        try:
            result = response.json()

        except ValueError as exc:

            self.logger.error(
                "LeetCode returned invalid JSON"
            )

            raise LeetCodeResponseError(
                "LeetCode returned an invalid JSON response"
            ) from exc

        # -----------------------------------------------------
        # Validate GraphQL response
        # -----------------------------------------------------

        if "errors" in result:

            errors = result["errors"]

            self.logger.error(
                "GraphQL errors: %s",
                errors,
            )

            raise LeetCodeAPIError(
                f"LeetCode GraphQL error: {errors}"
            )

        if "data" not in result:

            self.logger.error(
                "Unexpected GraphQL response: %s",
                result,
            )

            raise LeetCodeResponseError(
                "LeetCode response does not contain 'data'"
            )

        return result["data"]

    # =========================================================
    # Public Profile
    # =========================================================

    def get_profile(self, username: str) -> Dict[str, Any]:

        self._validate_username(username)

        query = """
        query userPublicProfile($username: String!) {
            matchedUser(username: $username) {

                username

                githubUrl
                twitterUrl
                linkedinUrl

                profile {
                    ranking
                    userAvatar
                    realName
                    aboutMe
                    school
                    websites
                    countryName
                    company
                    jobTitle
                    skillTags
                    postViewCount
                    reputation
                    solutionCount
                    categoryDiscussCount
                }
            }
        }
        """

        variables = {
            "username": username
        }

        data = self._query(
            query=query,
            variables=variables,
            operation_name="userPublicProfile",
        )

        matched_user = data.get("matchedUser")

        if matched_user is None:

            raise LeetCodeResponseError(
                f"LeetCode user '{username}' was not found"
            )

        return matched_user

    # =========================================================
    # Solved / Submission Statistics
    # =========================================================

    def get_stats(self, username: str) -> Dict[str, Any]:

        self._validate_username(username)

        query = """
        query userSessionProgress($username: String!) {

            allQuestionsCount {
                difficulty
                count
            }

            matchedUser(username: $username) {

                submitStats {

                    acSubmissionNum {
                        difficulty
                        count
                        submissions
                    }

                    totalSubmissionNum {
                        difficulty
                        count
                        submissions
                    }
                }
            }
        }
        """

        variables = {
            "username": username
        }

        data = self._query(
            query=query,
            variables=variables,
            operation_name="userSessionProgress",
        )

        matched_user = data.get("matchedUser")

        if matched_user is None:

            raise LeetCodeResponseError(
                f"LeetCode user '{username}' was not found"
            )

        return {
            "all_questions": data.get(
                "allQuestionsCount",
                []
            ),
            "user_stats": matched_user.get(
                "submitStats",
                {}
            ),
        }

    # =========================================================
    # Recent Accepted Submissions
    # =========================================================

    def get_recent_submissions(
        self,
        username: str,
        limit: int = 20,
    ) -> List[Dict[str, Any]]:

        self._validate_username(username)

        if limit <= 0:
            raise ValueError(
                "limit must be greater than 0"
            )

        # Public endpoint currently supports up to 20
        limit = min(limit, 20)

        query = """
        query recentAcSubmissions(
            $username: String!,
            $limit: Int!
        ) {

            recentAcSubmissionList(
                username: $username,
                limit: $limit
            ) {

                id
                title
                titleSlug
                timestamp
            }
        }
        """

        variables = {
            "username": username,
            "limit": limit,
        }

        data = self._query(
            query=query,
            variables=variables,
            operation_name="recentAcSubmissions",
        )

        submissions = data.get(
            "recentAcSubmissionList"
        )

        if submissions is None:

            raise LeetCodeResponseError(
                "Unexpected response: "
                "recentAcSubmissionList is missing"
            )

        return submissions

    # =========================================================
    # Fetch Everything
    # =========================================================

    def get_user_data(
        self,
        username: str,
    ) -> Dict[str, Any]:

        self.logger.info(
            "Fetching LeetCode data for user=%s",
            username,
        )

        profile = self.get_profile(username)

        stats = self.get_stats(username)

        recent_submissions = self.get_recent_submissions(
            username
        )

        return {
            "profile": profile,
            "stats": stats,
            "recent_submissions": recent_submissions,
        }

    # =========================================================
    # Validation
    # =========================================================

    
    @staticmethod
    def _validate_username(username: str) -> None:

        if not username:
            raise ValueError(
                "LeetCode username cannot be empty"
            )

        if not isinstance(username, str):
            raise TypeError(
                "LeetCode username must be a string"
            )

    def get_problem(
        self,
        title_slug: str,
    ) -> Dict[str, Any]:

        if not title_slug:
            raise ValueError(
                "title_slug cannot be empty"
            )

        query = """
        query questionData($titleSlug: String!) {

            question(titleSlug: $titleSlug) {

                questionId
                questionFrontendId

                title
                titleSlug

                difficulty

                isPaidOnly

                acRate

                topicTags {
                    name
                    slug
                }
            }
        }
        """

        variables = {
            "titleSlug": title_slug
        }

        data = self._query(
            query=query,
            variables=variables,
            operation_name="questionData",
        )

        question = data.get("question")

        if question is None:

            raise LeetCodeResponseError(
                f"LeetCode problem "
                f"'{title_slug}' was not found"
            )

        return question


    def get_user_status(self) -> Dict[str, Any]:

        query = """
        query userStatus {

            userStatus {

                isSignedIn

                username

                isPremium
            }
        }
        """

        data = self._query(
            query=query,
            variables={},
            operation_name="userStatus",
        )

        return data["userStatus"]


    def get_submission_history(
        self,
        limit: int = 20,
        offset: int = 0,
    ) -> Dict[str, Any]:

        if limit <= 0:
            raise ValueError(
                "limit must be greater than zero"
            )

        if offset < 0:
            raise ValueError(
                "offset cannot be negative"
            )

        query = """
        query submissionHistory(
            $offset: Int!
            $limit: Int!
        ) {

            submissionList(
                offset: $offset
                limit: $limit
            ) {

                submissions {
                    id
                    statusDisplay
                    lang
                    runtime
                    memory
                    timestamp
                    title
                    titleSlug
                }

                hasNext
            }
        }
        """

        data = self._query(
            query=query,
            variables={
                "offset": offset,
                "limit": limit,
            },
            operation_name="submissionHistory",
        )

        # print(
        #         "submission history response:",
        #         data
        #     )
        submission_list = data.get(
        "submissionList"
    )

        if submission_list is None:
            raise LeetCodeResponseError(
                "LeetCode returned no submissionList "
                f"for offset={offset}, limit={limit}"
            )

        submissions = submission_list.get(
            "submissions"
        )

        if submissions is None:
            raise LeetCodeResponseError(
                "LeetCode returned null submissions "
                f"for offset={offset}, limit={limit}"
            )

        return submission_list

    def iter_submission_history(
        self,
        page_size: int = 50,
    ):
        offset = 0

        while True:

            page = self.get_submission_history(
                limit=page_size,
                offset=offset,
            )

            submissions = page.get(
                "submissions"
            )

            if not submissions:
                break

            for submission in submissions:
                yield submission

            if not page.get(
                "hasNext",
                False,
            ):
                break

            offset += len(submissions)
    # =========================================================
    # Cleanup
    # =========================================================

    def close(self) -> None:

        self.logger.debug(
            "Closing LeetCode HTTP session"
        )

        self.session.close()

    def __enter__(self):

        return self

    def __exit__(
        self,
        exc_type,
        exc_value,
        traceback,
    ):

        self.close()