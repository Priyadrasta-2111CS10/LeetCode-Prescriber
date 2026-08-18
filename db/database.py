import os

import psycopg
from psycopg.rows import dict_row

class Database:

    def __init__(
        self,
        host: str = "localhost",
        port: int = 55432,
        database: str = "leettracker",
        user: str = "leettracker",
        password: str = "leettracker",
    ):
        self.connection_string = (
            f"host={host} "
            f"port={port} "
            f"dbname={database} "
            f"user={user} "
            f"password={password}"
        )

    def get_connection(self):

        return psycopg.connect(
            self.connection_string,
            row_factory=dict_row,
        )