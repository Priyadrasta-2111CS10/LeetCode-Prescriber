import logging
from typing import Any, Dict

import requests
from config import OLLAMA_BASE_URL, OLLAMA_MODEL, OLLAMA_TIMEOUT


class OllamaClient:

    def __init__(
        self,
        base_url: str = OLLAMA_BASE_URL,
        model: str = OLLAMA_MODEL,
        timeout: int = OLLAMA_TIMEOUT,

       
    ):

        self.base_url = base_url.rstrip("/")

        self.model = model

        self.timeout = timeout

        self.session = requests.Session()

        self.logger = logging.getLogger(
            self.__class__.__name__
        )


        self.logger.info(
            "Initialized OllamaClient: "
            "base_url=%s, model=%s, timeout=%s",
            self.base_url,
            self.model,
            self.timeout,
        )

        

    def generate(
        self,
        prompt: str,
    ) -> str:

        if not prompt:
            raise ValueError(
                "prompt cannot be empty"
            )

        url = (
            f"{self.base_url}/api/generate"
        )

        payload = {
            "model": self.model,

            "prompt": prompt,

            "stream": False,

            "format": "json",

            "options": {
                "temperature": 0.2,
                "num_predict": 700,
            },
        }

        self.logger.info(
            "Sending request to Ollama "
            "model=%s",
            self.model,
        )

        try:

            response = self.session.post(
                url,
                json=payload,
                timeout=self.timeout,
            )

            response.raise_for_status()

        except requests.RequestException as exc:

            self.logger.exception(
                "Ollama request failed"
            )

            raise RuntimeError(
                "Failed to communicate "
                "with Ollama"
            ) from exc

        data = response.json()

        result = data.get(
            "response"
        )

        if not result:

            raise RuntimeError(
                "Ollama returned an empty response"
            )

        return result

    def close(self):

        self.session.close()