import openmeteo_requests
import pandas as pd
import requests_cache
from retry_requests import retry
from read_metadata_table import get_sites

# Open-Meteo client setup
cache_session = requests_cache.CachedSession(".cache", expire_after=3600)

retry_session = retry(cache_session, retries=5, backoff_factor=0.2)

openmeteo = openmeteo_requests.Client(session=retry_session)

def get_weather(site_code, latitude, longitude):

    url = "https://api.open-meteo.com/v1/forecast"

    params = {
        "latitude": latitude,
        "longitude": longitude,
        "hourly": [
            "temperature_2m",
            "relative_humidity_2m",
            "direct_radiation_instant",
        ],
        "start_date": "2026-07-21",
        "end_date": "2026-07-28",
    }

    response = openmeteo.weather_api(url, params=params)[0]

    hourly = response.Hourly()

    temperature = hourly.Variables(0).ValuesAsNumpy()
    humidity = hourly.Variables(1).ValuesAsNumpy()
    radiation = hourly.Variables(2).ValuesAsNumpy()

    df = pd.DataFrame(
        {
            "site_code": site_code,
            "time_interval": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="right",
            ),
            "temperature": temperature,
            "humidity": humidity,
            "solar_radiance": radiation,
        }
    )

    return df

def get_data():

    sites = list(get_sites())

    BATCH_SIZE = 50

    all_weather_data = []

    success = 0
    failed = 0

    for i in range(0, len(sites), BATCH_SIZE):

        batch = sites[i : i + BATCH_SIZE]

        for site_code, latitude, longitude in batch:

            try:
                weather = get_weather(site_code, latitude, longitude)

                all_weather_data.append(weather)

                success += 1

            except Exception as e:

                failed += 1

    if all_weather_data:

        return pd.concat(all_weather_data, ignore_index=True)

    return pd.DataFrame()

























