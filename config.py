import os

from dotenv import load_dotenv


load_dotenv()


LEETCODE_SUBMISSION_PAGE_SIZE = int(
    os.getenv(
        "LEETCODE_SUBMISSION_PAGE_SIZE",
        "50",
    )
)

LEETCODE_INITIAL_SYNC_LIMIT = int(
    os.getenv(
        "LEETCODE_INITIAL_SYNC_LIMIT",
        "500",
    )
)

OLLAMA_BASE_URL = os.getenv(
    "OLLAMA_BASE_URL",
    "http://localhost:11434",
)

OLLAMA_MODEL = os.getenv(
    "OLLAMA_MODEL",
    "llama3.2:latest",
)

OLLAMA_TIMEOUT = int(
    os.getenv(
        "OLLAMA_TIMEOUT",
        "120",
    )
)

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

GEMINI_MODEL = os.getenv(
    "GEMINI_MODEL",
    "gemini-2.5-flash",
)

GEMINI_TIMEOUT = int(
    os.getenv(
        "GEMINI_TIMEOUT",
        "60",
    )
)