import logging
import time
from typing import TypeVar

from config import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_TIMEOUT
from google import genai
from google.genai import types
from google.genai.errors import ClientError
from pydantic import BaseModel

T = TypeVar(
    "T",
    bound=BaseModel,
)


class GeminiClient:

    MAX_RETRIES = 5

    def __init__(
        self,
        api_key: str = GEMINI_API_KEY,
        model: str = GEMINI_MODEL,
        timeout: int = GEMINI_TIMEOUT,
    ):

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured"
            )

        self.model = model

        self.client = genai.Client(
            api_key=api_key,
            http_options=types.HttpOptions(
                # Confirm units (ms vs s) against your installed
                # google-genai version before relying on this.
                timeout=timeout * 1000,
            ),
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def generate_structured(
        self,
        prompt: str,
        response_model: type[T],
    ) -> T:

        if not prompt:
            raise ValueError(
                "prompt cannot be empty"
            )

        interaction = self._create_interaction(
            prompt=prompt,
            response_model=response_model,
        )

        if not interaction.output_text:

            raise RuntimeError(
                "Gemini returned "
                "an empty response"
            )

        try:

            return (
                response_model
                .model_validate_json(
                    interaction.output_text
                )
            )

        except Exception as exc:

            self.logger.exception(
                "Gemini returned an invalid "
                "structured response"
            )

            raise RuntimeError(
                "Failed to validate "
                "Gemini response"
            ) from exc

    def _create_interaction(
        self,
        prompt: str,
        response_model: type[T],
    ):

        for attempt in range(self.MAX_RETRIES):

            self.logger.info(
                "Sending structured request "
                "to Gemini model=%s (attempt %d/%d)",
                self.model,
                attempt + 1,
                self.MAX_RETRIES,
            )

            try:

                return self.client.interactions.create(

                    model=self.model,

                    input=prompt,

                    response_format={
                        "type": "text",

                        "mime_type":
                            "application/json",

                        "schema":
                            response_model
                            .model_json_schema(),
                    },
                )

            except ClientError as exc:

                is_rate_limit = (
                    getattr(exc, "status_code", None) == 429
                )

                if not is_rate_limit or attempt == self.MAX_RETRIES - 1:

                    self.logger.exception(
                        "Gemini request failed"
                    )

                    raise RuntimeError(
                        "Failed to communicate "
                        "with Gemini"
                    ) from exc

                delay = (
                    self._extract_retry_delay(exc)
                    or (2 ** attempt)
                )

                self.logger.warning(
                    "Gemini rate limited, retrying "
                    "in %.1fs (attempt %d/%d)",
                    delay,
                    attempt + 1,
                    self.MAX_RETRIES,
                )

                time.sleep(delay)

            except Exception as exc:

                self.logger.exception(
                    "Gemini request failed"
                )

                raise RuntimeError(
                    "Failed to communicate "
                    "with Gemini"
                ) from exc

        raise RuntimeError(
            "Exceeded retries for "
            "generate_structured"
        )

    @staticmethod
    def _extract_retry_delay(exc: ClientError) -> float | None:

        try:

            details = exc.response.json()["error"]["details"]

            for detail in details:

                if detail.get("@type", "").endswith("RetryInfo"):

                    raw = detail["retryDelay"]

                    if raw.endswith("ms"):
                        return float(raw[:-2]) / 1000

                    return float(raw.rstrip("s"))

        except Exception:
            return None

        return None