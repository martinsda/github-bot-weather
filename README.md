# github-bot-weather
A twitter bot that displays weather

Follow-me @ [https://x.com/lxweatherbot](https://x.com/lxweatherbot)

Also prints the output of weather APIs in this readme.md file!

<div align="center">

## Currently
`Lisbon, Portugal - 2024-11-13 18:12:44`

<table>
    <tr>
        <th>Hour</th>
        <td>12 Hours</td>
    </tr>
    <tr>
        <th>Weather</th>
        <td><img src="http://openweathermap.org/img/wn/01d@2x.png"/></td>
    </tr>
    <tr>
        <th>Conditions</th>
        <td>Mainly Sunny</td>
    </tr>
    <tr>
        <th>Rain forecast</th>
        <td width="200px">20</td>
    </tr>
    <tr>
        <th>Rain probability</th>
        <td>5</td>
    </tr>
</table>

</div>


## Weather forcast 6AM to 11PM


<table>
    <tr>
        <th>Hour</th>
        <td> 6AM </td><td> 7AM </td><td> 8AM </td>
    </tr>
    <tr>
        <th>Weather</th>
        <td><img src="http://openweathermap.org/img/wn/02d@2x.png"/></td><td><img src="{{ 7AM_WEATHER_IMAGE }}"/></td><td><img src="{{ 8AM_WEATHER_IMAGE }}"/></td>
    </tr>
    <tr>
        <th>Conditions</th>
        <td>Partly Cloudy</td><td>{{ 7AM_WEATHER_CONDITIONS }}</td><td>{{ 8AM_WEATHER_CONDITIONS }}</td>
    </tr>
    <tr>
        <th>Rain forecast</th>
        <td width="200px">('0',)</td><td width="200px">{{ 7AM_RAIN_FORECAST }}</td><td width="200px">{{ 8AM_RAIN_FORECAST }}</td>
    </tr>
    <tr>
        <th>Rain probability</th>
        <td>(5,)</td><td>{{ 7AM_RAIN_PROBABILITY }}</td><td>{{ 8AM_RAIN_PROBABILITY }}</td>
    </tr>
</table>
