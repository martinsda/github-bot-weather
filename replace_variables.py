import os
import datetime
from datetime import datetime as dt
import pytz
import json

def get_weather_info(code, day_night='day'):
    with open('wmo_codes.json', 'r') as file:
        wmo_data = json.load(file)
    print(f"weather info for code {code}")
    if code in wmo_data:
        return wmo_data[code][day_night]
    else:
        return {"description": "Unknown code", "image": ""}

def get_weather_response(hour):
    with open('weatherdata.json', 'r') as file:
        weather_data = json.load(file)

    if 0<= hour <=23 :
        precipitation_probability = weather_data['precipitation_probability'][hour]
        precipitation = weather_data['precipitation'][hour]
        weather_code  = weather_data['weather_code'][hour]
        print(f"precipitation_prob {precipitation_probability} for hour {hour}")
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
    if now.hour >= 19:
        weather_info = get_weather_info(code,'night') 
    else:
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
        'HOUR_+2': str(int(os.getenv('HOUR_NOW', 0))+2),
        
        '6AM_WEATHER_IMAGE':  get_weather_info(get_weather_response(5)[2])['image'],
        '6AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(5)[2])['description'],
        '6AM_RAIN_FORECAST': str(get_weather_response(5)[1]),
        '6AM_RAIN_PROBABILITY': str(get_weather_response(5)[0]),
        '7AM_WEATHER_IMAGE':  get_weather_info(get_weather_response(6)[2])['image'],
        '7AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(6)[2])['description'],
        '7AM_RAIN_FORECAST': str(get_weather_response(6)[1]),
        '7AM_RAIN_PROBABILITY': str(get_weather_response(6)[0]),
        '8AM_WEATHER_IMAGE':  get_weather_info(get_weather_response(7)[2])['image'],
        '8AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(7)[2])['description'],
        '8AM_RAIN_FORECAST': str(get_weather_response(7)[1]),
        '8AM_RAIN_PROBABILITY': str(get_weather_response(7)[0]),

        '9AM_WEATHER_IMAGE':  get_weather_info(get_weather_response(8)[2])['image'],
        '9AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(8)[2])['description'],
        '9AM_RAIN_FORECAST': str(get_weather_response(8)[1]),
        '9AM_RAIN_PROBABILITY': str(get_weather_response(8)[0]),
        '10AM_WEATHER_IMAGE':  get_weather_info(get_weather_response(9)[2])['image'],
        '10AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(9)[2])['description'],
        '10AM_RAIN_FORECAST': str(get_weather_response(9)[1]),
        '10AM_RAIN_PROBABILITY': str(get_weather_response(9)[0]),
        '11AM_WEATHER_IMAGE':  get_weather_info(get_weather_response(10)[2])['image'],
        '11AM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(10)[2])['description'],
        '11AM_RAIN_FORECAST': str(get_weather_response(10)[1]),
        '11AM_RAIN_PROBABILITY': str(get_weather_response(10)[0]),

        '12PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(11)[2])['image'],
        '12PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(11)[2])['description'],
        '12PM_RAIN_FORECAST': str(get_weather_response(11)[1]),
        '12PM_RAIN_PROBABILITY': str(get_weather_response(11)[0]),
        '1PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(12)[2])['image'],
        '1PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(12)[2])['description'],
        '1PM_RAIN_FORECAST': str(get_weather_response(12)[1]),
        '1PM_RAIN_PROBABILITY': str(get_weather_response(12)[0]),
        '2PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(13)[2])['image'],
        '2PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(13)[2])['description'],
        '2PM_RAIN_FORECAST': str(get_weather_response(13)[1]),
        '2PM_RAIN_PROBABILITY': str(get_weather_response(13)[0]),

        '3PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(14)[2])['image'],
        '3PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(14)[2])['description'],
        '3PM_RAIN_FORECAST': str(get_weather_response(14)[1]),
        '3PM_RAIN_PROBABILITY': str(get_weather_response(14)[0]),
        '4PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(15)[2])['image'],
        '4PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(15)[2])['description'],
        '4PM_RAIN_FORECAST': str(get_weather_response(15)[1]),
        '4PM_RAIN_PROBABILITY': str(get_weather_response(15)[0]),
        '5PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(16)[2])['image'],
        '5PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(16)[2])['description'],
        '5PM_RAIN_FORECAST': str(get_weather_response(16)[1]),
        '5PM_RAIN_PROBABILITY': str(get_weather_response(16)[0]),

        '6PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(17)[2])['image'],
        '6PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(17)[2])['description'],
        '6PM_RAIN_FORECAST': str(get_weather_response(17)[1]),
        '6PM_RAIN_PROBABILITY': str(get_weather_response(17)[0]),
        '7PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(18)[2],'night')['image'],
        '7PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(18)[2],'night')['description'],
        '7PM_RAIN_FORECAST': str(get_weather_response(18)[1]),
        '7PM_RAIN_PROBABILITY': str(get_weather_response(18)[0]),
        '8PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(19)[2],'night')['image'],
        '8PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(19)[2],'night')['description'],
        '8PM_RAIN_FORECAST': str(get_weather_response(19)[1]),
        '8PM_RAIN_PROBABILITY': str(get_weather_response(19)[0]),

        '9PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(20)[2],'night')['image'],
        '9PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(20)[2],'night')['description'],
        '9PM_RAIN_FORECAST': str(get_weather_response(20)[1]),
        '9PM_RAIN_PROBABILITY': str(get_weather_response(20)[0]),
        '10PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(21)[2],'night')['image'],
        '10PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(21)[2],'night')['description'],
        '10PM_RAIN_FORECAST': str(get_weather_response(21)[1]),
        '10PM_RAIN_PROBABILITY': str(get_weather_response(21)[0]),
        '11PM_WEATHER_IMAGE':  get_weather_info(get_weather_response(22)[2],'night')['image'],
        '11PM_WEATHER_CONDITIONS': get_weather_info(get_weather_response(22)[2],'night')['description'],
        '11PM_RAIN_FORECAST': str(get_weather_response(22)[1]),
        '11PM_RAIN_PROBABILITY': str(get_weather_response(22)[0])
        
        # Add more variables as needed
    }
    replace_variables(template_path, output_path, variables)
