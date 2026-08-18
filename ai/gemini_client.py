import logging
from typing import TypeVar

from config import GEMINI_API_KEY, GEMINI_MODEL
from google import genai
from pydantic import BaseModel

T = TypeVar(
    "T",
    bound=BaseModel,
)


class GeminiClient:

    def __init__(
        self,
        api_key: str = GEMINI_API_KEY,
        model: str = GEMINI_MODEL,
    ):

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured"
            )

        self.model = model

        self.client = genai.Client(
            api_key=api_key
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

        self.logger.info(
            "Sending structured request "
            "to Gemini model=%s",
            self.model,
        )

        try:

            interaction = (
                self.client.interactions.create(

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
            )

        except Exception as exc:

            self.logger.exception(
                "Gemini request failed"
            )

            raise RuntimeError(
                "Failed to communicate "
                "with Gemini"
            ) from exc

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