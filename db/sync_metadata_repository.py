from typing import Optional

from db.database import Database


class SyncMetadataRepository:

    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def get_by_user_id(
        self,
        user_id: int,
        connection=None,
    ) -> Optional[dict]:

        query = """
            SELECT 
                id,
                user_id,
                last_sync_started_at,
                last_sync_completed_at,
                last_submission_timestamp,
                last_submission_id,
                sync_status,
                last_error
            FROM sync_metadata
            WHERE user_id = %s;
        """

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (user_id,),
                )

                return cursor.fetchone()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (user_id,),
                )

                return cursor.fetchone()

    def start_sync(
        self,
        user_id: int,
        connection: None, 
    ) -> dict:

        query = """
            INSERT INTO sync_metadata (
                user_id,
                last_sync_started_at,
                sync_status,
                last_error
            )
            VALUES (
                %s,
                NOW(),
                'RUNNING',
                NULL
            )
            ON CONFLICT (user_id)
            DO UPDATE SET
                last_sync_started_at = NOW(),
                sync_status = 'RUNNING',
                last_error = NULL
            RETURNING *;
        """

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (user_id,),
                )

                return cursor.fetchone()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (user_id,),
                )

                return cursor.fetchone()

    def complete_sync(
        self,
        user_id: int,
        submission_id: Optional[str],
        submission_timestamp,
        connection: None,
    ) -> dict:

        query = """
            UPDATE sync_metadata
            SET
                last_sync_completed_at = NOW(),
                last_submission_id = %s,
                last_submission_timestamp = %s,
                sync_status = 'SUCCESS',
                last_error = NULL
            WHERE user_id = %s
            RETURNING *;
        """
        if connection is not None:

            with connection.cursor() as cursor:
            
                            cursor.execute(
                                query,
                                (
                                    submission_id,
                                    submission_timestamp,
                                    user_id,
                                ),
                            )
            
                            return cursor.fetchone()


        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        submission_id,
                        submission_timestamp,
                        user_id,
                    ),
                )

                return cursor.fetchone()

    def fail_sync(
        self,
        user_id: int,
        error: str,
        connection : None
    ) -> None:

        query = """
            UPDATE sync_metadata
            SET
                sync_status = 'FAILED',
                last_error = %s
            WHERE user_id = %s;
        """
        if not connection:

             with connection.cursor() as cursor:
             
                             cursor.execute(
                                 query,
                                 (
                                     error,
                                     user_id,
                                 ),
                             )
                             
        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (
                        error,
                        user_id,
                    ),
                )