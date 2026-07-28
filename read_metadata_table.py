import psycopg


def get_sites():

    with psycopg.connect(
        dbname="meta", user="postgres", password="123789", host="localhost", port="5000"
    ) as conn:

        with conn.cursor() as cur:
            cur.execute("""
                SELECT site_name, latitude, longitude
                FROM metadata
            """)

            sites = cur.fetchall()

    print("Successfully data has been fetched")

    return sites


# sites = get_sites()

# for site_name, latitude, longitude in sites:
#     print(site_name, latitude, longitude)
