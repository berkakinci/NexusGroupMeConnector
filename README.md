FRC Nexus Provides event updates. This project uses Google App Engine to posting those to GroupMe.

# Set up Google App Engine:

This is free for low usage!

Setup info: https://cloud.google.com/appengine/docs/standard/python3/building-app

## Commands that'll help you get there in the end:

`gcloud init` # Only first time you set up

`gcloud app deploy`

## Other info you will need for `config.py`
- Start with defaults; fill `config.py` after other setup.
- The Nexus-Token for the nexus API.  You get this when setting up Nexus webhook, so you may have to come back to this later.
- The Bot ID from GroupMe.  You get this after setting up GroupMe Bot.

# Set up Nexus side:

https://frc.nexus/en/api

IIRC, the Nexus-Token was not available before setting up the first webhook.  This is a chicken-and-egg problem.  So the 'hello' page also accepts POST method, always responding with success.

Add the dummy webhook URL:<br>
https://GoogleAppEngineURL/<br>
Note the Nexus Token.

Set up a 'Push' API for real use:
- With the webhook URL as https://GoogleAppEngineURL/event
- Select 'All events'
- Select 'Match status for a specific team'

# Set up GroupMe side:

https://dev.groupme.com/bots

Create Bot:
- Callback URL is optional.  We do not use it.  Leave it blank.
- Avatar URL is optional.

Note the Bot ID
