import psycopg

def create_table_meta():
    try:
        with psycopg.connect(
            dbname="meta",
            user="postgres",
            password="123789",
            host="localhost",
            port="5000",
        ) as conn:

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS metadata (
                        site_name VARCHAR(100) Not NULL,
                        latitude DOUBLE PRECISION Not NULL,
                        longitude DOUBLE PRECISION Not NULL
                    );
                """)

            conn.commit()
            print("metadata table created.")

    except psycopg.Error as e:
        print(e)


def create_table_site_weather():
    try:
        with psycopg.connect(
            dbname="site_weather",
            user="postgres",
            password="123789",
            host="localhost",
            port="5000",
        ) as conn:

            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS site_weather (
                        site_name VARCHAR(100) Not NULL,
                        time_interval TIMESTAMPTZ Not NULL,
                        temperature REAL Not NULL,
                        humidity REAL Not NULL,
                        solar_radiace REAL Not NULL
                    );
                """)

            conn.commit()
            print("site_weather table created.")

    except psycopg.Error as e:
        print(e)
