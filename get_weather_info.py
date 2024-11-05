import json

def get_weather_info(code):
    with open('wmo_codes.json', 'r') as file:
        wmo_data = json.load(file)
    
    if code in wmo_data:
        return wmo_data[code]
    else:
        return {"description": "Unknown code", "image": ""}

if __name__ == "__main__":
    code = input("Enter WMO weather code: ")
    weather_info = get_weather_info(code)
    print(f"Description: {weather_info['description']}")
    print(f"Image URL: {weather_info['image']}")
