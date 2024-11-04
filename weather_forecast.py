# weather_forecast.py
import openmeteo_requests
import os
import requests_cache
import pandas as pd
from retry_requests import retry
import datetime

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
		"daily": ["temperature_2m_max", "temperature_2m_min", "sunrise", "sunset", "precipitation_sum", "precipitation_probability_max", "wind_speed_10m_max", "wind_gusts_10m_max", "wind_direction_10m_dominant"]
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
	daily_precipitation_sum = daily.Variables(4).ValuesAsNumpy()
	daily_precipitation_probability_max = daily.Variables(5).ValuesAsNumpy()
	daily_wind_speed_10m_max = daily.Variables(6).ValuesAsNumpy()
	daily_wind_gusts_10m_max = daily.Variables(7).ValuesAsNumpy()
	daily_wind_direction_10m_dominant = daily.Variables(8).ValuesAsNumpy()

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
	daily_data["precipitation_sum"] = daily_precipitation_sum
	daily_data["precipitation_probability_max"] = daily_precipitation_probability_max
	daily_data["wind_speed_10m_max"] = daily_wind_speed_10m_max
	daily_data["wind_gusts_10m_max"] = daily_wind_gusts_10m_max
	daily_data["wind_direction_10m_dominant"] = daily_wind_direction_10m_dominant

	daily_dataframe = pd.DataFrame(data = daily_data)
	print(daily_dataframe)
	return daily_dataframe 

def set_action_output(output_name, value):
    if "GITHUB_OUTPUT" in os.environ:
        with open(os.environ["GITHUB_OUTPUT"], "a") as f:
            print("{0}={1}".format(output_name, value), file=f)

def main():
    city_lat = os.getenv('OPEN_METEO_CITY_LAT')
    if city_lat:
        city_long = os.getenv('OPEN_METEO_CITY_LONG')
        if city_long:
            daily_dataframe = get_forecast_weather(city_lat, city_long)
            set_action_output('weather_forecast_date_0', daily_dataframe.date[0].strftime('%a'))
            set_action_output('weather_forecast_max_0', round(float(daily_dataframe.temperature_2m_max[0]), 1))
            set_action_output('weather_forecast_min_0', round(float(daily_dataframe.temperature_2m_min[0]), 1))
            if daily_dataframe.precipitation_sum[0] > 0:
                set_action_output('weather_forecast_rain_0', "Rain :" + str(round(float(daily_dataframe.precipitation_sum[0]), 1)) +" mm")
            else:
                set_action_output('weather_forecast_rain_0', "No rain")
            set_action_output('wind_speed_10m_0', "Wind: " + str(int(daily_dataframe.wind_speed_10m_max[0])) +" up to "+ str(int(daily_dataframe.wind_gusts_10m_max[0])) +" km/h " + str(round(float(daily_dataframe.wind_direction_10m_dominant[0]))) +"º")
            set_action_output('weather_forecast_date_1', daily_dataframe.date[1].strftime('%a'))
            set_action_output('weather_forecast_max_1', round(float(daily_dataframe.temperature_2m_max[1]), 1))
            set_action_output('weather_forecast_min_1', round(float(daily_dataframe.temperature_2m_min[1]), 1))
            if daily_dataframe.precipitation_sum[1] > 0:
                set_action_output('weather_forecast_rain_1', "Rain :"+ str(round(float(daily_dataframe.precipitation_sum[1]), 1)) +" mm")
            else:
                set_action_output('weather_forecast_rain_1', "No rain")
            set_action_output('wind_speed_10m_1', "Wind: " + str(int(daily_dataframe.wind_speed_10m_max[1])) +" up to "+str(int(daily_dataframe.wind_gusts_10m_max[1])) +" km/h " + str(round(float(daily_dataframe.wind_direction_10m_dominant[1])))+"º")
            set_action_output('weather_forecast_date_2', daily_dataframe.date[2].strftime('%a'))
            set_action_output('weather_forecast_max_2', round(float(daily_dataframe.temperature_2m_max[2]), 1))
            set_action_output('weather_forecast_min_2', round(float(daily_dataframe.temperature_2m_min[2]), 1))
            if daily_dataframe.precipitation_sum[2] > 0:
                set_action_output('weather_forecast_rain_2', "Rain :"+ str(round(float(daily_dataframe.precipitation_sum[2]), 1))+ " mm")
            else:
                set_action_output('weather_forecast_rain_2', "No rain")
            set_action_output('wind_speed_10m_2', "Wind: " + str(int(daily_dataframe.wind_speed_10m_max[2])) +" up to "+str(int(daily_dataframe.wind_gusts_10m_max[2])) +" km/h " + str(round(float(daily_dataframe.wind_direction_10m_dominant[2])))+"º")
            set_action_output('weather_forecast_date_3', daily_dataframe.date[3].strftime('%a'))
            set_action_output('weather_forecast_max_3', round(float(daily_dataframe.temperature_2m_max[3]), 1))
            set_action_output('weather_forecast_min_3', round(float(daily_dataframe.temperature_2m_min[3]), 1))
            if daily_dataframe.precipitation_sum[3] > 0:
                set_action_output('weather_forecast_rain_3', "Rain :"+ str(round(float(daily_dataframe.precipitation_sum[3]), 1)) +" mm")
            else:
                set_action_output('weather_forecast_rain_3', "No rain")
            set_action_output('wind_speed_10m_3', "Wind: " + str(int(daily_dataframe.wind_speed_10m_max[3])) +" up to "+str(int(daily_dataframe.wind_gusts_10m_max[3])) +" km/h " + str(round(float(daily_dataframe.wind_direction_10m_dominant[3])))+"º")
            set_action_output('weather_forecast_date_4', daily_dataframe.date[4].strftime('%a'))
            set_action_output('weather_forecast_max_4', round(float(daily_dataframe.temperature_2m_max[4]), 1))
            set_action_output('weather_forecast_min_4', round(float(daily_dataframe.temperature_2m_min[4]), 1))
            if daily_dataframe.precipitation_sum[4] > 0:
                set_action_output('weather_forecast_rain_4', "Rain :"+ str(round(float(daily_dataframe.precipitation_sum[4]), 1))+" mm")
            else:
                set_action_output('weather_forecast_rain_4', "No rain")
            set_action_output('wind_speed_10m_4', "Wind: " + str(int(daily_dataframe.wind_speed_10m_max[4])) +" up to "+str(int(daily_dataframe.wind_gusts_10m_max[4])) +" km/h " + str(round(float(daily_dataframe.wind_direction_10m_dominant[4])))+"º")
            set_action_output('weather_forecast_date_5', daily_dataframe.date[5].strftime('%a'))
            set_action_output('weather_forecast_max_5', round(float(daily_dataframe.temperature_2m_max[5]), 1))
            set_action_output('weather_forecast_min_5', round(float(daily_dataframe.temperature_2m_min[5]), 1))
            if daily_dataframe.precipitation_sum[5] > 0:
                set_action_output('weather_forecast_rain_5', "Rain :"+ str(round(float(daily_dataframe.precipitation_sum[5]), 1)) +" mm")
            else:
                set_action_output('weather_forecast_rain_5', "No rain")
            set_action_output('wind_speed_10m_5', "Wind: " + str(int(daily_dataframe.wind_speed_10m_max[5])) +" up to "+str(int(daily_dataframe.wind_gusts_10m_max[5])) +" km/h " + str(round(float(daily_dataframe.wind_direction_10m_dominant[5])))+"º")
        else:
            print("::error::Please set the OPEN_METEO_CITY_LONG environment variable.")
		
if __name__ == "__main__":
	main()
