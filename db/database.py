import os

import psycopg
from psycopg.rows import dict_row


class Database:

    def __init__(
        self,
        host: str = None,
        port: int = None,
        database: str = None,
        user: str = None,
        password: str = None,
    ):
        # Defaults match the local docker-compose.yml host-exposed port
        # (55432) so `python scripts/*.py` still works unchanged when run
        # directly on your machine. Inside Docker, DB_HOST/DB_PORT are set
        # explicitly to the internal service name/port (postgres:5432).
        self.connection_string = (
            f"host={host or os.getenv('DB_HOST', 'localhost')} "
            f"port={port or os.getenv('DB_PORT', '55432')} "
            f"dbname={database or os.getenv('DB_NAME', 'leettracker')} "
            f"user={user or os.getenv('DB_USER', 'leettracker')} "
            f"password={password or os.getenv('DB_PASSWORD', 'leettracker')}"
        )

    def get_connection(self):
        return psycopg.connect(
            self.connection_string,
            row_factory=dict_row,
        )

    def execute(
        self,
        query,
        params=None,
        connection=None,
        fetch=None,
    ):
        if connection is not None:
            return self._execute(connection, query, params, fetch)

        with self.get_connection() as connection:
            return self._execute(connection, query, params, fetch)

    @staticmethod
    def _execute(connection, query, params, fetch):
        with connection.cursor() as cursor:
            cursor.execute(query, params)

            if fetch == "one":
                return cursor.fetchone()

            if fetch == "all":
                return cursor.fetchall()

            return None
