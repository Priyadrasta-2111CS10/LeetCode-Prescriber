from ai.ollama_client import OllamaClient


def main():

    client = OllamaClient()

    try:

        response = client.generate(
            """
            Return valid JSON.

            Format:

            {
              "message": "hello"
            }
            """
        )

        print(
            "\n========== OLLAMA RESPONSE =========="
        )

        print(response)

    finally:

        client.close()


if __name__ == "__main__":
    main()