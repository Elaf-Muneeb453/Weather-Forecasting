import psycopg
from weather_api import get_data

def data_store():

    sites_df = get_data()

    with psycopg.connect(
        dbname="site_weather", 
        user="postgres", 
        password="123789",
        host="localhost", 
        port="5000"
    ) as conn:

        with conn.cursor() as cur:

            for _, row in sites_df.iterrows():

                cur.execute(
                    """
                    INSERT INTO site_weather
                    (site_name, time_interval, temperature, humidity, solar_radiance)
                    VALUES (%s, %s, %s, %s, %s)
                    """,
                    (row["site_code"], row["time_interval"], row["temperature"], row["humidity"], row["solar_radiance"]),
                )

        conn.commit()

    print("Site weather data inserted successfully!")