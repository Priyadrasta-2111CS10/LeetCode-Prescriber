from ai.gemini_embedding_client import GeminiEmbeddingClient


def main():

    client = GeminiEmbeddingClient()

    text = """
    Dynamic programming problem involving
    state transitions and optimal substructure.
    """

    embedding = client.embed(
        text
    )

    print(
        "Embedding dimension:",
        len(embedding),
    )

    print(
        "First 10 values:"
    )

    print(
        embedding[:10]
    )


if __name__ == "__main__":
    main()