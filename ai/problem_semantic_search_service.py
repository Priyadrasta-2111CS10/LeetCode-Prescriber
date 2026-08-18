class ProblemSemanticSearchService:

    def __init__(
        self,
        embedding_client,
        search_repository,
    ):

        self.embedding_client = (
            embedding_client
        )

        self.search_repository = (
            search_repository
        )

    def search(
        self,
        query: str,
        limit: int = 10,
    ):

        embedding = (
            self.embedding_client
            .embed(query)
        )

        return (
            self.search_repository
            .search(
                query_embedding=embedding,
                limit=limit,
            )
        )