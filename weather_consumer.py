# weather_consumer.py
import requests
import os

def get_weather(api_key, city):
	url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}"
	response = requests.get(url)
	if response.status_code == 200:
		data = response.json()
		weather_description = data['weather'][0]['description']
		temperature = data['main']['temp']
		return weather_description, temperature
	else:
		raise Exception(f"Failed to get weather data: {response.status_code}")

def main():
	api_key = os.getenv('OPENWEATHER_API_KEY')
	city = "Lisbon"
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
