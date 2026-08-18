from ai.gemini_client import GeminiClient


def main():

    client = GeminiClient()

    response = client.generate(
        """
        Return ONLY JSON.

        {
            "message": "hello"
        }
        """
    )

    print(
        "\n========== GEMINI RESPONSE =========="
    )

    print(response)


if __name__ == "__main__":
    main()