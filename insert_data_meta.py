import psycopg
from random_site_code import generate_site_data


def insert_sites():

    sites_df = generate_site_data(100)

    with psycopg.connect(
        dbname="meta", 
        user="postgres", 
        password="123789", 
        host="localhost", 
        port="5000"
    ) as conn:

        with conn.cursor() as cur:

            for _, row in sites_df.iterrows():

                cur.execute(
                    """
                    INSERT INTO metadata
                    (site_name, latitude, longitude)
                    VALUES (%s, %s, %s)
                    """,
                    (row["site_code"], row["latitude"], row["longitude"]),
                )

        conn.commit()

    print("Sites inserted successfully!")

