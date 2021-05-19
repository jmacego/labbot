import time
import requests
import json
import os
import re
from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound


omw_api_key = os.environ.get("OMW_KEY")
#omw_zip = os.environ.get("OMW_ZIP")

#influx = InfluxDBClient(config['influx']['host'], 8086, config['influx']['username'], config['influx']['password'], 'weather')
weather = Blueprint('weather', __name__, template_folder='templates/weather')
@weather.route('/weather', defaults={'page': 'current'})
@weather.route('/weather/current', methods=['POST'])
def get_weather():
    """Get the current weather
    """
    token = request.form.get('token', None)
    channel = request.form.get('channel_id', None)
    text = request.form.get('text', None)
    token2 = os.environ.get("SLACK_EVENTS_TOKEN")

    if token != token2:
        abort(403)

    args = text.split()

    unit = 'c'
    regex = re.compile("\d\d\d\d\d")
    if len(args) > 0:
        if len(args[0]) == 1:
            if ('f' in args[0] or 'c' in args[0] or 'k' in args[0]):
                unit = args[0]
        if regex.match(args[0]):
            owm_zip = args[0] + ",us"
    if len(args) > 1:
        if regex.match(args[1]):
            omw_zip = args[1] + ",us"
        
    weather = get_owm(omw_zip)
    temperature = Temperature(weather['main']['temp'])

    message = f"The current temperature is {getattr(temperature, unit):.1f}{unit.upper()}"
    print(text)
    return(message)
    #payload = {'text': json.dumps(request.form)}
    #return jsonify(payload)

def every(delay, task, *args, **kwargs):
    next_time = time.time() + delay
    print(time.time(), next_time)
    while True:
        time.sleep(max(0, next_time - time.time()))
        try:
            task(*args, **kwargs)
        except Exception:
            traceback.print_exc()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay

class Temperature:
    """Store a temperature and return"""
    def __init__(self, temp, unit="k"):
        """Store a temperature"""
        if unit == "c":
            self.k = self.__convert_c_to_k(temp)
            self.c = int(temp)
            self.f = self.__convert_k_to_f(self.k)
        elif unit == "f":
            self.k = self.__convert_f_to_k(temp)
            self.c = self.__convert_k_to_c(self.k)
            self.f = int(temp)
        elif unit == "k":
            self.k = int(temp)
            self.c = self.__convert_k_to_c(temp)
            self.f = self.__convert_k_to_f(temp)
        else:
            raise SystemError
    
    def __convert_c_to_k(self, c):
        """Convert a temperature from Celsius to Kelvin"""
        return c + 273.15
    
    def __convert_f_to_k(self, f):
        """Convert a temperature from Fahrenheit to Kelvin"""
        return (f - 32) * 5 / 9 + 273.15
    
    def __convert_k_to_f(self, k):
        """Convert a temperature from Kelvin to Fahrenheit"""
        return (k - 273.15) * 9 / 5 + 32
    
    def __convert_k_to_c(self, k):
        print(k)
        """Convert a temperature from Kelvin to Celsius"""
        return k - 273.15

def get_owm(omw_zip):
    complete_url = f"https://api.openweathermap.org/data/2.5/weather?zip={omw_zip}&appid={omw_api_key}"
    print(complete_url)
    response = requests.get(complete_url) 
    x = response.json() 
    if x["cod"] != "404": 
        return x

def temp():
    raw_data = get_owm()
    tags = { "city": "North Hollywood",
             "datasource": "OpenWeatherMaps",
             "state": "CA",
             "note:": "Commercial",
             "latitude": raw_data["coord"]["lat"],
             "longitude": raw_data["coord"]["lon"],}
    
    data = []
    
    data.append({"measurement": "sky",
                "tags": tags,
                "fields": {"value": raw_data["weather"][0]["main"]}
                })

    data.append({ "measurement": "temperature",
              "tags": tags,
              "fields": { "value": raw_data["main"]["temp"]}
              })
    data.append({ "measurement": "pressure",
              "tags": tags,
              "fields": { "value": raw_data["main"]["pressure"]}
              })
    data.append({ "measurement": "humidity",
              "tags": tags,
              "fields": { "value": raw_data["main"]["humidity"]}
              })
    data.append({ "measurement": "visibility",
              "tags": tags,
              "fields": { "value": raw_data["visibility"]}
              })
    data.append({ "measurement": "wind_speed",
              "tags": tags,
              "fields": { "value": raw_data["wind"]["speed"]}
              })
    data.append({ "measurement": "wind_direction",
              "tags": tags,
              "fields": { "value": raw_data["wind"]["deg"]}
              })
    data.append({ "measurement": "clouds",
              "tags": tags,
              "fields": { "value": raw_data["clouds"]["all"]}
              })

    return data
