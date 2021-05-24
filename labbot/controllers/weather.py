"""Get weather from OpenWeather Map"""
import time
import os
import re
import requests
from flask import Blueprint, request
from labbot.controllers import utils


omw_api_key = os.environ.get("OMW_KEY")

#influx = InfluxDBClient(config['influx']['host'], 8086, config['influx']\
# ['username'], config['influx']['password'], 'weather')
weather = Blueprint('weather', __name__, template_folder='templates/weather')
@weather.route('/weather', defaults={'page': 'current'})
@weather.route('/weather/current', methods=['POST'])
def get_weather():
    """Get the current weather
    """

    utils.validate_token(request.form.get('token', None))
    text = request.form.get('text', None)
    #channel = request.form.get('channel_id', None)
    args = text.split()
    omw_zip = os.environ.get("OMW_ZIP")

    unit = 'c'
    regex = re.compile(r"\d\d\d\d\d")
    if len(args) > 0:
        if len(args[0]) == 1:
            if ('f' in args[0] or 'c' in args[0] or 'k' in args[0]):
                unit = args[0]
        if regex.match(args[0]):
            omw_zip = args[0] + ",us"
    if len(args) > 1:
        if regex.match(args[1]):
            omw_zip = args[1] + ",us"

    omw_weather = get_owm(omw_zip)
    temperature = Temperature(omw_weather['main']['temp'])

    message = f"The current temperature is {getattr(temperature, unit):.1f}{unit.upper()}"
    print(text)
    return message
    #payload = {'text': json.dumps(request.form)}
    #return jsonify(payload)

def every(delay, task, *args, **kwargs):
    """Perform action every x"""
    next_time = time.time() + delay
    print(time.time(), next_time)
    while True:
        time.sleep(max(0, next_time - time.time()))
        #try:
        task(*args, **kwargs)
        #except Exception:
        #    traceback.print_exception()
            # in production code you might want to have this instead of course:
            # logger.exception("Problem while executing repetitive task.")
        # skip tasks if we are behind schedule:
        next_time += (time.time() - next_time) // delay * delay + delay

class Temperature:
    """Store a temperature and return"""
    def __init__(self, temp, unit="k"):
        """Store a temperature"""
        if unit == "c":
            self.temp_kelvin = convert_c_to_k(temp)
        elif unit == "f":
            self.temp_kelvin = convert_f_to_k(temp)
        elif unit == "k":
            self.temp_kelvin = int(temp)
        else:
            raise SystemError

    def get_fahrenheit(self):
        """Return Fahrenheit"""
        return convert_k_to_f(self.temp_kelvin)

    def get_celsius(self):
        """Return Celsius"""
        return convert_k_to_c(self.temp_kelvin)

    def get_kelvin(self):
        """Return Kelvin"""
        return self.temp_kelvin


def convert_c_to_k(celsius):
    """Convert a temperature from Celsius to Kelvin"""
    return celsius + 273.15

def convert_f_to_k(fahrenheit):
    """Convert a temperature from Fahrenheit to Kelvin"""
    return (fahrenheit - 32) * 5 / 9 + 273.15

def convert_k_to_f(kelvin):
    """Convert a temperature from Kelvin to Fahrenheit"""
    return (kelvin - 273.15) * 9 / 5 + 32

def convert_k_to_c(kelvin):
    """Convert a temperature from Kelvin to Celsius"""
    return kelvin - 273.15

def get_owm(omw_zip):
    """Get the JSON from OMW"""
    base_url = "https://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}zip={omw_zip}&appid={omw_api_key}"
    print(complete_url)
    response = requests.get(complete_url)
    response_json = response.json()
    if response_json["cod"] != "404":
        return response_json
    return None

def influx_temp(omw_zip):
    """Some deprecated specific data for Influx"""
    raw_data = get_owm(omw_zip)
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
