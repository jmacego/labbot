import random
from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound
import json
import os

class CoinBot:

    # Create a constant that contains the default text for the message
    COIN_BLOCK = {
        "type": "section",
        "text": {
            "type": "mrkdwn",
            "text": (
                "Sure! Flipping a coin...\n\n"
            ),
        },
    }

    # The constructor for the class. It takes a channel name as a
    # parameter and sets it as an instance variable.
    def __init__(self, channel):
        self.channel = channel
    
    def _flip_coin(self):
        rand_int = random.randint(0,1)
        if rand_int == 0:
            results = "Heads"
        else:
            results = "Tails"
        
        text = f"The result is {results}"

        return text
    
    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        coin_flip = self._flip_coin()
        return {
            "channel": self.channel,
            "text": coin_flip,
            "blocks": [
                self.COIN_BLOCK,
                {"type": "section", "text": { "type": "mrkdwn", "text": coin_flip}}
            ],
        }

coin = Blueprint('coin', __name__, template_folder='templates/coin')
@coin.route('/coin', defaults={'page': 'flip'})
@coin.route('/coin/flip', methods=['POST'])
def flip_coin():
    """Craft the CoinBot, flip the coin, and send the message to the channel
    """
    token = request.form.get('token', None)
    channel = request.form.get('channel_id', None)
    text = request.form.get('text', None)
    token2 = os.environ.get("SLACK_EVENTS_TOKEN")

    if token != token2:
        abort(403)
    # Create a new CoinBot
    coin_bot = CoinBot(channel)

    # Get the onboarding message payload
    message = coin_bot.get_message_payload()

    # Post the onboarding message in Slack
    #slack_web_client.chat_postMessage(**message)
    #print(message)
    return(message)
    #payload = {'text': json.dumps(request.form)}
    #return jsonify(payload)


if __name__ == "__main__":
    from slack_sdk.web import WebClient
    import os

    # Create a slack client
    slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

    # Get a new CoinBot
    #coin_bot = CoinBot("#testing")
    coin_bot = CoinBot("U021L1T8MAT")

    # Get the onboarding message payload
    message = coin_bot.get_message_payload()

    # Post the onboarding message in slack
    slack_web_client.chat_postMessage(**message)