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
    
    responses = openmeteo.weather_api(url, params=params)

    response = responses[0]
    hourly = response.Hourly()
    temperature = hourly.Variables(0).ValuesAsNumpy()
    humidity = hourly.Variables(1).ValuesAsNumpy()
    radiation = hourly.Variables(2).ValuesAsNumpy()

    hourly_dataframe = pd.DataFrame(
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
    
    return hourly_dataframe

def get_data():
    sites = get_sites()
    all_weather_data = []

    for site_code, latitude, longitude in sites:
        weather_df = get_weather(site_code, latitude, longitude)
        all_weather_data.append(weather_df)

    final_dataframe = pd.concat(all_weather_data, ignore_index=True)
    # final_dataframe.to_csv("all_sites_weather.csv", index=False)

    return final_dataframe

