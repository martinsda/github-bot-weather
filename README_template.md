# github-bot-weather
A twitter bot that displays weather

Follow-me @ [https://x.com/lxweatherbot](https://x.com/lxweatherbot)

Also prints the output of weather APIs in this readme.md file!

<div align="center">

## Currently
`{{ CITY }}, {{ COUNTRY }} - {{ DATE_TIME }}`

<table>
    <tr>
        <th>Hour</th>
        <td>{{ HOUR_NOW }} Hours</td>
    </tr>
    <tr>
        <th>Weather</th>
        <td><img src="{{ CURR_WEATHER_IMAGE }}"/></td>
    </tr>
    <tr>
        <th>Conditions</th>
        <td>{{ CURR_WEATHER_CONDITIONS }}</td>
    </tr>
    <tr>
        <th>Rain forecast</th>
        <td width="200px">{{ RAIN_FORECAST }}</td>
    </tr>
    <tr>
        <th>Rain probability</th>
        <td>{{ RAIN_PROBABILITY }}</td>
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
        <td><img src="{{ 6AM_WEATHER_IMAGE }}"/></td><td><img src="{{ 7AM_WEATHER_IMAGE }}"/></td><td><img src="{{ 8AM_WEATHER_IMAGE }}"/></td>
    </tr>
    <tr>
        <th>Conditions</th>
        <td>{{ 6AM_WEATHER_CONDITIONS }}</td><td>{{ 7AM_WEATHER_CONDITIONS }}</td><td>{{ 8AM_WEATHER_CONDITIONS }}</td>
    </tr>
    <tr>
        <th>Rain forecast</th>
        <td width="200px">{{ 6AM_RAIN_FORECAST }} mm</td><td width="200px">{{ 7AM_RAIN_FORECAST }} mm</td><td width="200px">{{ 8AM_RAIN_FORECAST }} mm</td>
    </tr>
    <tr>
        <th>Rain probability</th>
        <td>{{ 6AM_RAIN_PROBABILITY }}%</td><td>{{ 7AM_RAIN_PROBABILITY }}%</td><td>{{ 8AM_RAIN_PROBABILITY }}%</td>
    </tr>
</table>
