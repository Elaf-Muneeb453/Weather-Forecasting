# import openmeteo_requests

# import pandas as pd
# import requests_cache
# from retry_requests import retry
# from read_metadata_table import get_sites


# # Setup the Open-Meteo API client with cache and retry on error
# cache_session = requests_cache.CachedSession(".cache", expire_after=3600)
# retry_session = retry(cache_session, retries=5, backoff_factor=0.2)
# openmeteo = openmeteo_requests.Client(session=retry_session)

# # Make sure all required weather variables are listed here
# # The order of variables in hourly or daily is important to assign them correctly below
# url = "https://api.open-meteo.com/v1/forecast"
# params = {
#     "latitude": 52.52,
#     "longitude": 13.41,
#     "hourly": ["temperature_2m", "relative_humidity_2m", "direct_radiation_instant"],
#     "start_date": "2026-07-20",
#     "end_date": "2026-07-28",
# }
# responses = openmeteo.weather_api(url, params=params)

# # Process first location. Add a for-loop for multiple locations or weather models
# response = responses[0]
# print(f"Coordinates: {response.Latitude()}°N {response.Longitude()}°E")
# print(f"Elevation: {response.Elevation()} m asl")
# print(f"Timezone difference to GMT+0: {response.UtcOffsetSeconds()}s")

# # Process hourly data. The order of variables needs to be the same as requested.
# hourly = response.Hourly()
# hourly_temperature_2m = hourly.Variables(0).ValuesAsNumpy()
# hourly_relative_humidity_2m = hourly.Variables(1).ValuesAsNumpy()
# hourly_direct_radiation_instant = hourly.Variables(2).ValuesAsNumpy()

# hourly_data = {
#     "date": pd.date_range(
#         start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
#         end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
#         freq=pd.Timedelta(seconds=hourly.Interval()),
#         inclusive="left",
#     )
# }

# hourly_data["temperature_2m"] = hourly_temperature_2m
# hourly_data["relative_humidity_2m"] = hourly_relative_humidity_2m
# hourly_data["direct_radiation_instant"] = hourly_direct_radiation_instant

# hourly_dataframe = pd.DataFrame(data=hourly_data)
# hourly_dataframe.to_csv("eight_das.csv")
# print("\nHourly data\n", hourly_dataframe)


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
            "solar_radiation": radiation,
        }
    )

    return hourly_dataframe

sites = get_sites()

all_weather_data = []


for site_code, latitude, longitude in sites:

    print(f"Fetching weather for {site_code}")
    weather_df = get_weather(site_code, latitude, longitude)
    all_weather_data.append(weather_df)


final_dataframe = pd.concat(all_weather_data, ignore_index=True)


print(final_dataframe)

# Optional save
final_dataframe.to_csv("all_sites_weather.csv", index=False)
