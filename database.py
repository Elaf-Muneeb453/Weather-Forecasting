import psycopg
from psycopg import sql


def create_postgres_db_1(db_name):
    try:
        # 1. Connect to the default system database 'postgres'
        # 2. Explicitly set autocommit=True to prevent automatic transaction blocks
        with psycopg.connect(
            dbname="csv_database",
            user="postgres",
            password="123789",
            host="localhost",
            port="5000",
            autocommit=True,
        ) as conn:

            with conn.cursor() as cur:
                # Use the sql module to safely build the query and avoid SQL injection
                query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cur.execute(query)
                print(f"Database '{db_name}' created successfully!")

    except psycopg.Error as e:
        print(f"An error occurred: {e}")


def create_postgres_db_2(db_name):
    try:
        # 1. Connect to the default system database 'postgres'
        # 2. Explicitly set autocommit=True to prevent automatic transaction blocks
        with psycopg.connect(
            dbname="csv_database",
            user="postgres",
            password="123789",
            host="localhost",
            port="5000",
            autocommit=True,
        ) as conn:

            with conn.cursor() as cur:
                # Use the sql module to safely build the query and avoid SQL injection
                query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cur.execute(query)
                print(f"Database '{db_name}' created successfully!")

    except psycopg.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    create_postgres_db_1("meta")
    create_postgres_db_2("site_weather")
    
