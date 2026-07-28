import psycopg
from psycopg import sql
from create_tables import create_table_meta, create_table_site_weather
from insert_data_meta import insert_sites


def create_db_meta(db_name):
    try:
        with psycopg.connect(
            dbname="csv_database",
            user="postgres",
            password="123789",
            host="localhost",
            port="5000",
            autocommit=True,
        ) as conn:
            with conn.cursor() as cur:
                query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cur.execute(query)
                print(f"Database '{db_name}' created successfully!")

    except psycopg.Error as e:
        print(f"An error occurred: {e}")


def create_db_site_weather(db_name):
    try:
        with psycopg.connect(
            dbname="csv_database",
            user="postgres",
            password="123789",
            host="localhost",
            port="5000",
            autocommit=True,
        ) as conn:

            with conn.cursor() as cur:
                query = sql.SQL("CREATE DATABASE {}").format(sql.Identifier(db_name))
                cur.execute(query)
                print(f"Database '{db_name}' created successfully!")

    except psycopg.Error as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    # create_db_meta("meta")
    # create_db_site_weather("site_weather")
    create_table_meta()
    # create_table_site_weather()
    insert_sites()
