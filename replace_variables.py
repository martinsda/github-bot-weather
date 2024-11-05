import os
import datetime
from datetime import datetime as dt
import pytz
import json

def get_weather_info(code):
    with open('wmo_codes.json', 'r') as file:
        wmo_data = json.load(file)
    
    if code in wmo_data:
        return wmo_data[code]
    else:
        return {"description": "Unknown code", "image": ""}

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
        # Add more variables as needed
    }
    replace_variables(template_path, output_path, variables)
