"""Flask App for LabBot"""
import os
import logging
import json
import requests
from flask import Flask, render_template, Blueprint, abort, jsonify
from jinja2 import TemplateNotFound
from slack_sdk.web import WebClient
from slackeventsapi import SlackEventAdapter
from labbot.controllers import apphome
from labbot.controllers.coinbot import coin
from labbot.controllers import coinbot
from labbot.controllers.weather import weather
from labbot.controllers.misc import misc
from labbot.controllers.onboarding import onboarding
#from labbot.database import db_session

#from .controllers.apphome import apphome

# Initialize the Flask App to host the event adapter
app = Flask(__name__)
app.config.from_mapping(
    SQLALCHEMY_DATABASE_URI="sqlite:///" + os.path.join(app.instance_path, 'labbot.sqlite'),
                       )

# Create an events adapter and register it to an endpoint in the slack app for event ingestion.
slack_events_adapter = SlackEventAdapter(os.environ.get("SLACK_SIGNING_SECRET"),
                                                        "/slack/events", app)

# Initialize a Web API client
slack_web_client = WebClient(token=os.environ.get("SLACK_TOKEN"))

app.register_blueprint(coin)
app.register_blueprint(weather)
app.register_blueprint(misc)
app.register_blueprint(apphome.apphome)
app.register_blueprint(onboarding)

#@app.teardown_appcontext
#def shutdown_session():
#    """Cleanly kill the db session"""
#    db_session.remove()


# ================ Team Join Event =============== #
# When the user first joins a team, the type of the event will be 'team_join'.
# Here we'll link the onboarding_message callback to the 'team_join' event.
@slack_events_adapter.on("team_join")
def onboarding_message(payload):
    """Create and send an onboarding welcome message to new users. Save the
    time stamp of this message so we can update this message in the future.
    """
    #event = payload.get("event", {})

    # Get the id of the Slack user associated with the incoming event
    #user_id = event.get("user", {}).get("id")

    # Open a DM with the new user.
    #response = slack_web_client.conversations_open(users=user_id)
    #channel = response["channel"]["id"]
    return payload

# ============= Reaction Added Events ============= #
# When a users adds an emoji reaction to the onboarding message,
# the type of the event will be 'reaction_added'.
# Here we'll link the update_emoji callback to the 'reaction_added' event.
@slack_events_adapter.on("reaction_added")
def update_emoji(payload):
    """Update the onboarding welcome message after receiving a "reaction_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    #event = payload.get("event", {})

    #channel_id = event.get("item", {}).get("channel")
    #user_id = event.get("user")
    return payload


# =============== Pin Added Events ================ #
# When a users pins a message the type of the event will be 'pin_added'.
# Here we'll link the update_pin callback to the 'reaction_added' event.
@slack_events_adapter.on("pin_added")
def update_pin(payload):
    """Update the onboarding welcome message after receiving a "pin_added"
    event from Slack. Update timestamp for welcome message as well.
    """
    #event = payload.get("event", {})

    #channel_id = event.get("channel_id")
    #user_id = event.get("user")
    return payload


# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("message")
def message(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """

    event = payload.get("event", {})

    channel_id = event.get("channel")
    #user_id = event.get("user")
    text = event.get("text")

    # Check and see if the activation phrase was in the text of the message.
    # If so, execute the code to flip a coin.
    if "bot, flip a coin" in text.lower():
        # Since the activation phrase was met, get the channel ID that the event
        # was executed on
        channel_id = event.get("channel")

        # Execute the flip_coin function and send the results of
        # flipping a coin to the channel

        # Post the onboarding message in Slack
        print("Coin Flip")
        reply_message = coinbot.flip_coin(channel_id)
        result = slack_web_client.chat_postMessage(**reply_message)
        return result
    if text and text.lower() == "start":
        print("Start onboarding")
        # This was a user doing the tutorial
        result = "This isn't a thing yet"
        return result

    print("Unknown payload")
    print(json.dumps(json.loads(payload), indent=2))
    return -1

# When a 'message' event is detected by the events adapter, forward that payload
# to this function.
@slack_events_adapter.on("app_home_opened")
def app_home_opened(payload):
    """Parse the message event, and if the activation string is in the text,
    simulate a coin flip and send the result.
    """

    apphome.app_home_opened(payload)

if __name__ == "__main__":
    # Create the logging object
    logger = logging.getLogger()

    # Set the log level to DEBUG. This will increase the verbosity of logging messages
    logger.setLevel(logging.DEBUG)

    # Add the StreamHandler as a logging handler
    logger.addHandler(logging.StreamHandler())

    # Run your app on yor externally facing IP address on port 3000 instead of
    # running it on localhost, which is traditional for development.
    app.run(host='0.0.0.0', port=3000)
