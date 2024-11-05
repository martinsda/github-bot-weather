# weather_hourlyforecast.py
import openmeteo_requests
import os
import requests_cache
import pandas as pd
from retry_requests import retry
import datetime
from datetime import datetime as dt

def get_forecast_weather(lat, long):
  # Setup the Open-Meteo API client with cache and retry on error
  cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
  retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
  openmeteo = openmeteo_requests.Client(session = retry_session)
  
  # Make sure all required weather variables are listed here
  # The order of variables in hourly or daily is important to assign them correctly below
  url = "https://api.open-meteo.com/v1/forecast"
  params = {
  	"latitude": lat,
  	"longitude": long,
  	"hourly": ["precipitation_probability", "precipitation"],
	"forecast_days": 1
  }
  responses = openmeteo.weather_api(url, params=params)
  
  # Process first location. Add a for-loop for multiple locations or weather models
  response = responses[0]
  print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
  print(f"Elevation {response.Elevation()} m asl")
  print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
  print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")
  
  # Process hourly data. The order of variables needs to be the same as requested.
  hourly = response.Hourly()
  hourly_precipitation_probability = hourly.Variables(0).ValuesAsNumpy()
  hourly_precipitation = hourly.Variables(1).ValuesAsNumpy()
  
  hourly_data = {"date": pd.date_range(
  	start = pd.to_datetime(hourly.Time(), unit = "s", utc = True),
  	end = pd.to_datetime(hourly.TimeEnd(), unit = "s", utc = True),
  	freq = pd.Timedelta(seconds = hourly.Interval()),
  	inclusive = "left"
  )}
  hourly_data["precipitation_probability"] = hourly_precipitation_probability
  hourly_data["precipitation"] = hourly_precipitation
  
  hourly_dataframe = pd.DataFrame(data = hourly_data)
  print(hourly_dataframe)
  return hourly_dataframe 

def set_action_output(output_name, value):
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format(output_name, value), file=f)

def main():
    city_lat = os.getenv('OPEN_METEO_CITY_LAT')
    if city_lat:
        city_long = os.getenv('OPEN_METEO_CITY_LONG')
        if city_long:
            hourly_dataframe = get_forecast_weather(city_lat, city_long)
            now = dt.now()
            print(f"Hour now: {now.hour} ")
            set_action_output('weather_forecast_now_hour', now.hour)
            if hourly_dataframe.precipitation[now.hour] > 0:
                    set_action_output('weather_forecast_rain_now_sum', "" + str(round(float(hourly_dataframe.precipitation[now.hour]), 1)) +" mm")
            else:
                    set_action_output('weather_forecast_rain_now_sum', "No rain")
            if hourly_dataframe.precipitation_probability[now.hour] > 0:
                    set_action_output('weather_forecast_rain_now_prob', "" + str(round(float(hourly_dataframe.precipitation_probability[now.hour]), 1)) +"%")
            else:
                set_action_output('weather_forecast_rain_now_prob', "0%")
        else:
            print("::error::Please set the OPEN_METEO_CITY_LONG environment variable.")
    else:
            print("::error::Please set the OPEN_METEO_CITY_LAT environment variable.")
		
if __name__ == "__main__":
	main()