import os
import json
import requests
from flask import Blueprint
apphome = Blueprint('apphome', __name__, template_folder='templates/apphome')
@apphome.route('/apphome', defaults={'page': 'index'})
@apphome.route('/apphome/index', methods=['POST'])
def index():
    pass

def app_home_opened(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """

    event = payload.get("event", {})

    channel_id = event.get("channel")
    user_id = event.get("user")
    text = event.get("text")
    APP_HOME_BLOCK = {
                        "user_id": user_id,
                        "view": {
                            "type":"home",
                            "blocks":[
                                {
                                    "type":"section",
                                    "text":{
                                        "type":"mrkdwn",
                                        "text":"""
Civilization, as we know it, will end sometime this evening.
See SYSNOTE tomorrow for more information."""
                                    }
                                }
                            ]
                            }
                        }

    url = 'https://slack.com/api/views.publish'
    headers = { "Content-type": "application/json",
                "AUTHORIZATION": "Bearer " + os.environ.get("SLACK_TOKEN") }

    x = requests.post(url, headers= headers, data = json.dumps(APP_HOME_BLOCK))