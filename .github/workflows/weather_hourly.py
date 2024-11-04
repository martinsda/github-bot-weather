name: Weather Hourly Consumer

on:
  #push:
  #  branches:
  #    - main
  release:
    types: [published]
  schedule:
    - cron: '10 * * * *'  # Runs every hour at minute 10

jobs:
  run-hourly-weather-consumer:
    runs-on: ubuntu-latest

    steps:
    - name: Checkout repository
      uses: actions/checkout@v2

    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.x'

    - name: Install dependencies
      run: |
        python -m pip install --upgrade pip
        pip install requests
        pip install openmeteo-requests
        pip install requests-cache retry-requests numpy pandas

    - name: Run weather hourly forecast script
      id: forecast
      env:
        OPEN_METEO_CITY_LAT: ${{ vars.OPEN_METEO_CITY_LAT }}
        OPEN_METEO_CITY_LONG: ${{ vars.OPEN_METEO_CITY_LONG }}
      run: |
        python weather_hourlyforecast.py

    - name: Display forecast data
      if: ${{ steps.forecast.weather_forecast_rain_now_sum <> 'No rain' }}
      run| 
        echo "Next hour in #${{ vars.CITY }} ☔ alert:
        echo "Rain forecast: ${{ steps.forecast.outputs.weather_forecast_rain_now_sum }} mm"
        echo "Rain probability: ${{ steps.forecast.outputs.weather_forecast_rainprob_0 }}"


        
        
    
        
