from typing import Optional

from db.database import Database
from models import User
from psycopg.types.json import Jsonb


class UserRepository:

    def __init__(
        self,
        database: Database,
    ):
        self.database = database

    def save(self, user: User, connection=None,) -> dict:

        query = """
            INSERT INTO users (
                username,
                ranking,
                real_name,
                about_me,
                school,
                country_name,
                company,
                job_title,
                github_url,
                twitter_url,
                linkedin_url,
                avatar_url,
                websites,
                skill_tags,
                reputation,
                solution_count,
                category_discuss_count
            )
            VALUES (
                %(username)s,
                %(ranking)s,
                %(real_name)s,
                %(about_me)s,
                %(school)s,
                %(country_name)s,
                %(company)s,
                %(job_title)s,
                %(github_url)s,
                %(twitter_url)s,
                %(linkedin_url)s,
                %(avatar_url)s,
                %(websites)s,
                %(skill_tags)s,
                %(reputation)s,
                %(solution_count)s,
                %(category_discuss_count)s
            )
            ON CONFLICT (username)
            DO UPDATE SET
                ranking = EXCLUDED.ranking,
                real_name = EXCLUDED.real_name,
                about_me = EXCLUDED.about_me,
                school = EXCLUDED.school,
                country_name = EXCLUDED.country_name,
                company = EXCLUDED.company,
                job_title = EXCLUDED.job_title,
                github_url = EXCLUDED.github_url,
                twitter_url = EXCLUDED.twitter_url,
                linkedin_url = EXCLUDED.linkedin_url,
                avatar_url = EXCLUDED.avatar_url,
                websites = EXCLUDED.websites,
                skill_tags = EXCLUDED.skill_tags,
                reputation = EXCLUDED.reputation,
                solution_count = EXCLUDED.solution_count,
                category_discuss_count =
                    EXCLUDED.category_discuss_count,
                updated_at = NOW()
            RETURNING *;
        """

        params = {
            "username": user.username,
            "ranking": user.ranking,
            "real_name": user.real_name,
            "about_me": user.about_me,
            "school": user.school,
            "country_name": user.country_name,
            "company": user.company,
            "job_title": user.job_title,
            "github_url": user.github_url,
            "twitter_url": user.twitter_url,
            "linkedin_url": user.linkedin_url,
            "avatar_url": user.avatar_url,
            "websites": Jsonb(user.websites or []),
            "skill_tags": Jsonb(user.skill_tags or []),
            "reputation": user.reputation,
            "solution_count": user.solution_count,
            "category_discuss_count":
                user.category_discuss_count,
        }

        if connection is not None:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params,
                )

                return cursor.fetchone()

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    params,
                )

                return cursor.fetchone()

    def find_by_username(
        self,
        username: str,
    ) -> Optional[dict]:

        query = """
            SELECT *
            FROM users
            WHERE username = %s;
        """

        with self.database.get_connection() as connection:

            with connection.cursor() as cursor:

                cursor.execute(
                    query,
                    (username,),
                )

                return cursor.fetchone()