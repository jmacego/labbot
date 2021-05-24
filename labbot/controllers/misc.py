"""Misc utilities!"""
import os
from flask import Blueprint, request
from labbot.controllers import utils

misc = Blueprint('misc', __name__, template_folder='templates/misc')
@misc.route('/misc', defaults={'page': 'index'})
@misc.route('/misc/index', methods=['POST'])
def index():
    """Blank index page, still don't know why"""

@misc.route('/misc/fortune', methods=['POST'])
def fortune():
    """Get fortune
    """
    utils.validate_token(request.form.get('token', None))

    #channel = request.form.get('channel_id', None)
    #text = request.form.get('text', None)

    fortune_str = os.popen('fortune').read()
    print(fortune_str)
    #str(fortune_str)
    #print(type(fortune_str))
    return fortune_str
