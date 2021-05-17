import random

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

        return {"type": "section", "text": { "type": "mrkdwn", "text": text}},
    
    # Craft and return the entire message payload as a dictionary.
    def get_message_payload(self):
        return {
            "channel": self.channel,
            "blocks": [
                self.COIN_BLOCK,
                *self._flip_coin(),
            ],
        }


def flip_coin(channel):
    """Craft the CoinBot, flip the coin, and send the message to the channel
    """

    # Create a new CoinBot
    coin_bot = CoinBot(channel)

    # Get the onboarding message payload
    message = coin_bot.get_message_payload()

    # Post the onboarding message in Slack
    #slack_web_client.chat_postMessage(**message)
    return(message)


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