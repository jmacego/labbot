"""Misc utilities needed by multiple controllers"""
import os
from flask import abort

def validate_token(slack_token):
    """Compare the token, abort if no match"""
    local_token = os.environ.get("SLACK_EVENTS_TOKEN")

    if slack_token != local_token:
        abort(403)

    return True
