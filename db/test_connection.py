from db.database import Database


def main():

    database = Database()

    with database.get_connection() as connection:

        with connection.cursor() as cursor:

            cursor.execute("""
                SELECT table_name
                FROM information_schema.tables
                WHERE table_schema = 'public'
                ORDER BY table_name;
            """)

            tables = cursor.fetchall()

            print("PostgreSQL connection successful!\n")

            print("Tables:")

            for table in tables:
                print(
                    f" - {table['table_name']}"
                )


if __name__ == "__main__":
    main()