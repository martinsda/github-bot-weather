# weather_forecast.py
import openmeteo_requests

import requests_cache
import pandas as pd
from retry_requests import retry

# Lisbon "latitude":  38.7167,
#	"longitude": -9.1333,
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
		"daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "rain_sum", "wind_speed_10m_max", "wind_gusts_10m_max"]
	}
	responses = openmeteo.weather_api(url, params=params)

	# Process first location. Add a for-loop for multiple locations or weather models
	response = responses[0]
	print(f"Coordinates {response.Latitude()}°N {response.Longitude()}°E")
	print(f"Elevation {response.Elevation()} m asl")
	print(f"Timezone {response.Timezone()} {response.TimezoneAbbreviation()}")
	print(f"Timezone difference to GMT+0 {response.UtcOffsetSeconds()} s")

	# Process daily data. The order of variables needs to be the same as requested.
	daily = response.Daily()
	daily_temperature_2m_max = daily.Variables(0).ValuesAsNumpy()
	daily_temperature_2m_min = daily.Variables(1).ValuesAsNumpy()
	daily_sunrise = daily.Variables(2).ValuesAsNumpy()
	daily_sunset = daily.Variables(3).ValuesAsNumpy()
	daily_rain_sum = daily.Variables(4).ValuesAsNumpy()
	daily_wind_speed_10m_max = daily.Variables(5).ValuesAsNumpy()
	daily_wind_gusts_10m_max = daily.Variables(6).ValuesAsNumpy()

	daily_data = {"date": pd.date_range(
		start = pd.to_datetime(daily.Time(), unit = "s", utc = True),
		end = pd.to_datetime(daily.TimeEnd(), unit = "s", utc = True),
		freq = pd.Timedelta(seconds = daily.Interval()),
		inclusive = "left"
	)}
	daily_data["temperature_2m_max"] = daily_temperature_2m_max
	daily_data["temperature_2m_min"] = daily_temperature_2m_min
	daily_data["sunrise"] = daily_sunrise
	daily_data["sunset"] = daily_sunset
	daily_data["rain_sum"] = daily_rain_sum
	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
	daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max

	daily_dataframe = pd.DataFrame(data = daily_data)
	print(daily_dataframe)
	return daily_dataframe 

def main():
    city_lat = os.getenv('OPEN_METEO_CITY_LAT')
    if city_lat:
        city_long = os.getenv('OPEN_METEO_CITY_LONG')
        if city_long:
            daily_dataframe = get_forecast_weather(city_lat, city_long)
            print(f"::set-output name=weather_forecast_max_0::{daily_dataframe.temperature_2m_max[0]}")
        else:
            print("::error::Please set the OPEN_METEO_CITY_LONG environment variable.")
    else:
        print("::error::Please set the OPEN_METEO_CITY_LAT environment variable.")


if __name__ == "__main__":
	main()
