from flask import Flask, request
import google.cloud.logging
import logging

from groupme import GroupMe
from nexus import Nexus

# Local config file
import config

### Globals
# Set up Google Cloud Logging
client = google.cloud.logging.Client()
client.setup_logging()

# If `entrypoint` is not defined in app.yaml, App Engine will look for an app
# called `app` in `main.py`.
app = Flask(__name__)

groupme = GroupMe(config.groupme_bot_id)
nexus = Nexus(config.nexus_token,
              config.timezone)

@app.route("/", methods=['GET', 'POST'])
def hello():
    """Return a happy HTTP greeting.

    Returns:
        A string.
    """
    # For authentication debug, uncomment.
    #debug_info = f'{request.headers=}'
    #debug_info += f'{request.data=}'
    #debug_info += f'{request.json=}'
    #logging.info(debug_info)

    return "Nexus to GroupMe connector.  Expecting Event info POSTs at /event."

@app.route("/event", methods=['POST', 'GET'])
def handle_incoming_event():
    """Handle incoming Nexus events.
    Allowing GET for dumb debug.
    We require pre-determined Nexus-Token to take any action.

    Returns:
        Success, Happy Text.
    """

    # For authentication debug, uncomment.
    #debug_info = f'{request.headers=}'
    #debug_info += f'{request.data=}'
    #debug_info += f'{request.json=}'
    #logging.info(debug_info)

    # Authentication
    #nexus.abort_unless_authenticated(request.headers,
    #                                 "Only Nexus is allowed to post events")
    if not nexus.is_authenticated(request.headers):
        return "Not Authenticated.  Nexus-Token didn't match."

    # If we are here, we have a legitimate event
    #debug_info = f'{request.headers=}'
    #debug_info = f'{request.data=}'
    debug_info = f'{request.json=}'
    logging.info(debug_info)

    message = nexus.pretty(request.get_json())
    result = groupme.post_message(f"{message}")
    debug_info = f'POST to GroupMe {result=}'
    logging.info(debug_info)

    return "Got it!"
