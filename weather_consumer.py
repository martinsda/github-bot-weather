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
		wind_kmph = round(wind_speed * 3.6 , 1)
		print("temperature", temperature, "city", city)
		return weather_description, temperature, temp_min, temp_max, wind_speed, wind_deg, wind_kmph
	else:
		raise Exception(f"Failed to get weather data: {response.status_code}")

def set_action_output(output_name, value) :
    if "GITHUB_OUTPUT" in os.environ :
        with open(os.environ["GITHUB_OUTPUT"], "a") as f :
            print("{0}={1}".format(output_name, value), file=f)
		
def main():
	api_key = os.getenv('OPENWEATHER_API_KEY')
	if api_key:
		city = os.getenv('OPENWEATHER_API_CITY')
		if city:
			try:
				weather_description, temperature,  temp_min, temp_max, wind_speed, wind_deg, wind_kmph = get_weather(api_key, city)
				set_action_output('weather_description',weather_description)
				set_action_output('temperature',temperature)
				set_action_output('temp_min',temp_min)
				set_action_output('temp_max',temp_max)
				set_action_output('wind_speed',wind_speed)
				set_action_output('wind_kmph',wind_kmph)
				set_action_output('wind_deg',wind_deg)
			except Exception as e:
				print(f"::error::{str(e)}")
		else:
			print("::error::Please set the OPENWEATHER_API_CITY environment variable.")
	else:
		print("::error::Please set the OPENWEATHER_API_KEY environment variable.")

if __name__ == "__main__":
	main()
