import logging

from google import genai
from google.genai import types

from config import GEMINI_API_KEY


class GeminiEmbeddingClient:

    MODEL = "gemini-embedding-2"

    DIMENSIONS = 1536

    def __init__(
        self,
        api_key: str = GEMINI_API_KEY,
    ):

        if not api_key:
            raise ValueError(
                "GEMINI_API_KEY is not configured"
            )

        self.client = genai.Client(
            api_key=api_key
        )

        self.logger = logging.getLogger(
            self.__class__.__name__
        )

    def embed(
        self,
        text: str,
    ) -> list[float]:

        results = self.embed_many(
            [text]
        )

        return results[0]

    def embed_many(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        contents = [
        types.Content(
            parts=[
                types.Part.from_text(
                    text=text
                )
            ]
        )
        for text in texts
    ]

        response = (
            self.client.models.embed_content(

                model=self.MODEL,

                contents=contents,

                config=types.EmbedContentConfig(
                    output_dimensionality=(
                        self.DIMENSIONS
                    )
                ),
            )
        )

        if not response.embeddings:

            raise RuntimeError(
                "Gemini returned no embeddings"
            )

        return [
            embedding.values
            for embedding
            in response.embeddings
        ]