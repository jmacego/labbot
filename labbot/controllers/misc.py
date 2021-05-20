import os
from flask import Blueprint, render_template, abort, request, jsonify
from jinja2 import TemplateNotFound

misc = Blueprint('misc', __name__, template_folder='templates/misc')
@misc.route('/misc', defaults={'page': 'index'})
@misc.route('/misc/index', methods=['POST'])
def index():
    pass

@misc.route('/misc/fortune', methods=['POST'])
def fortune():
    """Get fortune
    """
    token = request.form.get('token', None)
    channel = request.form.get('channel_id', None)
    text = request.form.get('text', None)
    token2 = os.environ.get("SLACK_EVENTS_TOKEN")

    if token != token2:
        abort(403)
    
    fortune = os.popen('fortune').read()
    print(fortune)
    str(fortune)
    print(type(fortune))
    return fortune