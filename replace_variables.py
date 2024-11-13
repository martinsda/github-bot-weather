import os
import datetime
from datetime import datetime as dt
import pytz
import json

def get_weather_info(code):
    with open('wmo_codes.json', 'r') as file:
        wmo_data = json.load(file)
    
    if code in wmo_data:
        return wmo_data[code]['day']
    else:
        return {"description": "Unknown code", "image": ""}

def get_weather_response(hour):
    with open('weatherdata.json', 'r') as file:
        weather_data = json.load(file)

    if 0<= hour <=23 :
        precipitation_probability = weather_data["precipitation_probability"][hour],
        precipitation = weather_data["precipitation"][hour],
        weather_code  = weather_data["weather_code"][hour]
        return precipitation_probability, precipitation, weather_code
    else:
        return "Invalid hour, please enter a value between 0 and 23."

def replace_variables(template_path, output_path, variables):
    with open(template_path, 'r') as file:
        content = file.read()

    for key, value in variables.items():
        content = content.replace(f'{{{{ {key} }}}}', value)

    with open(output_path, 'w') as file:
        file.write(content)

if __name__ == "__main__":
    now = dt.now(pytz.timezone('Europe/Lisbon'))
    
    template_path = os.getenv('TEMPLATE_PATH')
    output_path = os.getenv('OUTPUT_PATH')
    code =  os.getenv('WEATHER_CODE')
    weather_info = get_weather_info(code)
    variables = {
        'CITY': os.getenv('CITY'),
        'COUNTRY': os.getenv('COUNTRY'),
        'DATE_TIME': now.strftime("%Y-%m-%d %H:%M:%S"),
        'CURR_WEATHER_CONDITIONS': weather_info['description'],
        'CURR_WEATHER_IMAGE': weather_info['image'],
        'RAIN_FORECAST': os.getenv('RAIN_FORECAST'),
        'RAIN_PROBABILITY': os.getenv('RAIN_PROBABILITY'),
        'HOUR_NOW': os.getenv('HOUR_NOW'),
        'HOUR_+1': str(int(os.getenv('HOUR_NOW', 0))+1),
        'HOUR_+2': str(int(os.getenv('HOUR_NOW', 0))+2)
        '6AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(5).weather_code)['description']
        
        # Add more variables as needed
    }
    replace_variables(template_path, output_path, variables)
