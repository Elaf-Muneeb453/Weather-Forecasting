import pandas as pd
import psycopg 

hostname = "localhost"
port=5000
database_name="weather_forecasting"
server_name="postgres"
pwd ="123789"


conn = psycopg.connect(
    host=hostname,
    port=5000,
    dbname=database_name,  # or another existing database
    user=server_name,
    password=pwd,
    autocommit=True,
)
