#!/home/polo/pyenvs/wttr/bin/python

import json
import requests
from datetime import datetime

WEATHER_CODES = {
    '113': '',
    '116': '',
    '119': '',
    '122': '',
    '143': '',
    '176': '󰼳',
    '179': '󰼴',
    '182': '󰼵',
    '185': '󰖗',
    '200': '',
    '227': '',
    '230': '',
    '248': '',
    '260': '',
    '263': '',
    '266': '',
    '281': '',
    '284': '',
    '293': '󰖗',
    '296': '󰖗',
    '299': '',
    '302': '',
    '305': '',
    '308': '',
    '311': '',
    '314': '',
    '317': '',
    '320': '',
    '323': '',
    '326': '',
    '329': '',
    '332': '',
    '335': '',
    '338': '',
    '350': '󰼩',
    '353': '',
    '356': '',
    '359': '',
    '362': '',
    '365': '',
    '368': '󰖘',
    '371': '',
    '374': '',
    '377': '',
    '386': '',
    '389': '',
    '392': '',
    '395': ''
}

data = {}


weather = requests.get("https://wttr.in/Hamburg?format=j1").json()


def format_time(time):
    return time.replace("00", "").zfill(2)


def format_temp(temp):
    return (hour['FeelsLikeC']+"°").ljust(3)


def format_chances(hour):
    chances = {
        "chanceoffog": "Fog",
        "chanceoffrost": "Frost",
        "chanceofovercast": "Overcast",
        "chanceofrain": "Rain",
        "chanceofsnow": "Snow",
        "chanceofsunshine": "Sunshine",
        "chanceofthunder": "Thunder",
        "chanceofwindy": "Wind"
    }

    conditions = []
    for event in chances.keys():
        if int(hour[event]) > 0:
            conditions.append(chances[event]+" "+hour[event]+"%")
    return ", ".join(conditions)

current = weather["current_condition"][0]
tempint = int(current['FeelsLikeC'])
extrachar = ''
if tempint > 0 and tempint < 10:
    extrachar = '+'


data['text'] = extrachar+current['FeelsLikeC']+"°" + WEATHER_CODES[current['weatherCode']] 

data['tooltip'] = f"<b>{current['weatherDesc'][0]['value']} {current['temp_C']}°</b>\n"
data['tooltip'] += f"Feels like: {current['FeelsLikeC']}°\n"
data['tooltip'] += f"Wind: {current['windspeedKmph']}Km/h\n"
data['tooltip'] += f"Humidity: {current['humidity']}%\n"
for i, day in enumerate(weather['weather']):
    data['tooltip'] += f"\n<b>"
    if i == 0:
        data['tooltip'] += "Today, "
    if i == 1:
        data['tooltip'] += "Tomorrow, "
    data['tooltip'] += f"{day['date']}</b>\n"
    data['tooltip'] += f" {day['maxtempC']}°  {day['mintempC']}° "
    data['tooltip'] += f"   {day['astronomy'][0]['sunrise']}    {day['astronomy'][0]['sunset']}\n"
    for hour in day['hourly']:
        if i == 0:
            if int(format_time(hour['time'])) < datetime.now().hour-2:
                continue
        data['tooltip'] += f"{format_time(hour['time'])}   {format_temp(hour['FeelsLikeF'])} {WEATHER_CODES[hour['weatherCode']]}   {hour['weatherDesc'][0]['value']}, {format_chances(hour)}\n"


print(json.dumps(data))
