# weather_consumer.py
import requests
import os

def get_weather(api_key, city):
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		weather_description = data['weather'][0]['description']
		temperature = data['main']['temp']
		temp_min = data['main']['temp_min']
		temp_max = data['main']['temp_max'] 
		wind_speed = data['wind']['speed'] 
		wind_deg = data['wind']['deg'] 
		return weather_description, temperature, temp_min, temp_max, wind_speed, wind_deg
	else:
		raise Exception(f"Failed to get weather data: {response.status_code}")

def main():
	api_key = os.getenv('OPENWEATHER_API_KEY')
	city = os.getenv('OPENWEATHER_CITY')
	if api_key:
		try:
			weather_description, temperature = get_weather(api_key, city)
			print(f"::set-output name=weather_description::{weather_description}")
			print(f"::set-output name=temperature::{temperature}")
		except Exception as e:
			print(f"::error::{str(e)}")
	else:
		print("::error::Please set the OPENWEATHER_API_KEY environment variable.")

if __name__ == "__main__":
	main()
