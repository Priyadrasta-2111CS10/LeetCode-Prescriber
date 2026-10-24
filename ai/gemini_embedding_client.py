import logging
import time

from google import genai
from google.genai import types
from google.genai.errors import ClientError

from config import GEMINI_API_KEY


class DailyQuotaExceededError(RuntimeError):
    """Raised when Gemini's PER-DAY embedding quota is exhausted —
    distinct from a per-minute rate limit, which IS worth retrying.
    Callers (like ProblemEmbeddingService.embed_all) should catch this
    specifically and stop entirely for the day, rather than treating it
    as a per-batch failure and pointlessly retrying every remaining
    batch, each of which will fail identically until the quota resets.
    """


class GeminiEmbeddingClient:

    MODEL = "gemini-embedding-2"
    DIMENSIONS = 1536

    MAX_RETRIES = 3
    RATE_LIMIT_WAIT_SECONDS = 60

    def __init__(self, api_key: str = GEMINI_API_KEY):

        if not api_key:
            raise ValueError("GEMINI_API_KEY is not configured")

        self.client = genai.Client(api_key=api_key)
        self.logger = logging.getLogger(self.__class__.__name__)

    def embed(self, text: str) -> list[float]:
        return self.embed_many([text])[0]

    def embed_many(self, texts: list[str]) -> list[list[float]]:

        if not texts:
            return []

        contents = [
            types.Content(parts=[types.Part.from_text(text=text)])
            for text in texts
        ]

        for attempt in range(self.MAX_RETRIES):

            try:
                response = self.client.models.embed_content(
                    model=self.MODEL,
                    contents=contents,
                    config=types.EmbedContentConfig(
                        output_dimensionality=self.DIMENSIONS
                    ),
                )

                if not response.embeddings:
                    raise RuntimeError("Gemini returned no embeddings")

                return [e.values for e in response.embeddings]

            except ClientError as exc:

                is_rate_limit = getattr(exc, "status_code", None) == 429
                is_daily_quota = self._is_daily_quota_error(exc)

                if is_daily_quota:
                    self.logger.error(
                        "Daily embedding quota exhausted for model=%s.",
                        self.MODEL,
                    )
                    raise DailyQuotaExceededError(
                        "Gemini daily embedding quota exhausted for "
                        f"today ({len(texts)}-item batch)."
                    ) from exc

                if not is_rate_limit or attempt == self.MAX_RETRIES - 1:
                    raise

                self.logger.warning(
                    "Rate limited (%d items), halting %ds before "
                    "retry (attempt %d/%d)",
                    len(texts), self.RATE_LIMIT_WAIT_SECONDS,
                    attempt + 1, self.MAX_RETRIES,
                )
                time.sleep(self.RATE_LIMIT_WAIT_SECONDS)

        raise RuntimeError("Exceeded retries for embed_many")

    @staticmethod
    def _is_daily_quota_error(exc: ClientError) -> bool:
        try:
            details = exc.response.json()["error"]["details"]
            for detail in details:
                for violation in detail.get("violations", []):
                    if "PerDay" in violation.get("quotaId", ""):
                        return True
        except Exception:
            pass
        return False