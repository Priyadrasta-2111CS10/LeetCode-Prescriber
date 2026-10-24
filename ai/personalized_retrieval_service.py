from models import ProblemCandidate


class PersonalizedRetrievalService:

    def __init__(
        self,
        user_repository,
        search_repository,
        embedding_client,
        recommendation_repository,
        topic_embedding_repository=None,  # see note below
    ):

        self.user_repository = user_repository
        self.search_repository = search_repository
        self.embedding_client = embedding_client
        self.recommendation_repository = recommendation_repository
        self.topic_embedding_repository = topic_embedding_repository

        # In-process cache as a fallback/first layer even without a DB-backed
        # cache — cheap, and covers repeated calls within one running process.
        self._embedding_cache: dict[str, list[float]] = {}

    def retrieve(self, username, topic, acceptance_rate, limit=20):
        user = self.user_repository.find_by_username(username)
        if user is None:
            raise ValueError(f"User '{username}' not found")

        query_embedding = self._get_topic_embedding(topic)

        rows = self.search_repository.search_personalized(
            user_id=user["id"],
            topic=topic,
            query_embedding=query_embedding,
            limit=limit,
        )

        return [self._to_candidate(row) for row in rows]

    def retrieve_many(self, username, topics, limit=20):
        user = self.user_repository.find_by_username(username)
        if user is None:
            raise ValueError(f"User '{username}' not found")

        user_id = user["id"]

        recently_recommended_ids = (
            self.recommendation_repository.get_recently_recommended_problem_ids(
                user_id=user_id,
                days=30,
            )
        )

        # Resolve embeddings per unique topic — cached wherever possible,
        # embedded fresh only for topics never seen before (in this
        # process, or ever, if a DB-backed cache is wired in).
        topic_embeddings = self._get_topic_embeddings(
            [topic for topic, _ in topics]
        )

        results = []

        for topic, acceptance_rate in topics:
            query_embedding = topic_embeddings[topic]

            rows = self.search_repository.search_personalized(
                user_id=user_id,
                topic=topic,
                query_embedding=query_embedding,
                # Over-fetch because some will be removed from
                # recommendation history.
                limit=limit * 2,
            )

            raw_candidates = [self._to_candidate(row) for row in rows]

            candidates = [
                c for c in raw_candidates
                if c.problem_id not in recently_recommended_ids
            ]

            if not candidates:
                candidates = raw_candidates

            candidates = candidates[:limit]

            results.append({
                "topic": topic,
                "acceptance_rate": acceptance_rate,
                "candidates": candidates,
            })

        return results

    def _get_topic_embedding(self, topic: str) -> list[float]:
        return self._get_topic_embeddings([topic])[topic]

    def _get_topic_embeddings(self, topics: list[str]) -> dict[str, list[float]]:
        """
        Returns a {topic: embedding} map, resolving each topic from
        (in priority order): the in-process cache, the DB-backed cache
        (if configured), or a fresh Gemini call — only for topics that
        genuinely aren't cached anywhere yet.
        """
        unique_topics = list(dict.fromkeys(topics))  # de-dupe, preserve order
        result: dict[str, list[float]] = {}
        missing: list[str] = []

        for topic in unique_topics:
            if topic in self._embedding_cache:
                result[topic] = self._embedding_cache[topic]
            else:
                missing.append(topic)

        if missing and self.topic_embedding_repository is not None:
            still_missing = []
            for topic in missing:
                cached = self.topic_embedding_repository.find_by_topic(topic)
                if cached is not None:
                    result[topic] = cached
                    self._embedding_cache[topic] = cached
                else:
                    still_missing.append(topic)
            missing = still_missing

        if missing:
            queries = [self._build_query(topic) for topic in missing]
            embeddings = self.embedding_client.embed_many(queries)

            if len(embeddings) != len(missing):
                raise RuntimeError(
                    "Embedding count does not match topic count"
                )

            for topic, embedding in zip(missing, embeddings):
                result[topic] = embedding
                self._embedding_cache[topic] = embedding

                if self.topic_embedding_repository is not None:
                    self.topic_embedding_repository.save(topic, embedding)

        return result

    @staticmethod
    def _build_query(topic: str) -> str:
        # Deliberately does NOT include acceptance_rate — that number
        # changes on nearly every call and would otherwise defeat
        # caching for no real retrieval-quality benefit. Acceptance
        # rate still reaches the LLM in the recommendation prompt
        # (problem_recommender.py), where it's genuinely useful context;
        # it just doesn't belong in the embedded *search* text.
        return f"""
        LeetCode interview practice.

        Topic:
        {topic}

        Focus on problems involving:
        - {topic}
        - core patterns of {topic}
        - interview-oriented applications
        - appropriate problem-solving techniques

        Find problems that build strong fundamentals in this topic.
        """.strip()

    @staticmethod
    def _to_candidate(row) -> ProblemCandidate:
        return ProblemCandidate(
            problem_id=row["problem_id"],
            title=row["title"],
            title_slug=row["title_slug"],
            difficulty=row["difficulty"],
            topics=row["topics"],
            previous_attempts=row["previous_attempts"] or 0,
            previous_accepted_attempts=row["previous_accepted_attempts"] or 0,
            similarity=float(row["similarity"]),
            last_attempted_at=row["last_attempted_at"],
        )