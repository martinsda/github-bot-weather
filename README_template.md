# github-bot-weather
A twitter bot that displays weather

Follow-me @ [https://x.com/lxweatherbot](https://x.com/lxweatherbot)

Also prints the output of weather APIs in this readme.md file!

<div align="center">

`{{ CITY }}, {{ COUNTRY }} - {{ DATE_TIME }}`

{{ CURR_WEATHER_CONDITIONS }}

</div>


## Weather For Next 3 hours


<table>
    <tr>
        <th>Hour</th>
        <td>{{ HOUR_NOW }}</td><td>{{ HOUR_+1 }}</td><td>{{ HOUR_+2 }}</td>
    </tr>
    <tr>
        <th>Weather</th>
        <td><img src="https://cdn.weatherapi.com/weather/64x64/day/116.png"/></td><td><img src="https://cdn.weatherapi.com/weather/64x64/day/176.png"/></td><td><img src="https://cdn.weatherapi.com/weather/64x64/day/116.png"/></td>
    </tr>
    <tr>
        <th>Rain forecast</th>
        <td width="200px">{{ RAIN_FORECAST }}</td><td width="200px">Patchy rain nearby</td><td width="200px">Partly Cloudy </td>
    </tr>
    <tr>
        <th>Rain probability</th>
        <td>{{ RAIN_PROBABILITY }}</td><td>21.6 -  25.4 °C</td><td>22 -  28.3 °C</td>
    </tr>
    <tr>
        <th>Wind</th>
        <td>1.2 kph</td><td>11.2 kph</td><td>10.4 kph</td>
    </tr>
</table>
