from flask import abort
from pprint import PrettyPrinter
from datetime import datetime
from zoneinfo import ZoneInfo

class Nexus:
    """
    Nexus interface.
    """
    pp_for_message = PrettyPrinter(width=40,
                                   indent=2,
                                   compact=False)
    include_date = False
    recursion_limit = 3

    def __init__(self,
                 nexus_token,
                 timezone):
        self.nexus_token = nexus_token
        self.timezone = ZoneInfo(timezone)
        return

    def abort_unless_authenticated(self,
                                   headers,
                                   extra_message=''):
        "Checks Authentication token.  Aborts on authentication failure"
        if not self.is_authenticated(headers):
            abort(401, f"Not Authorized.  {extra_message}")
        return

    def is_authenticated(self,
                         headers):
        "Checks Authentication token.  Returns boolean."
        got_token = headers.get('Nexus-Token')
        if not got_token == self.nexus_token:
            return False
        return True

    def _time_to_human(self,
                       obj,
                       _depth=1):
        "Converts timestamps to human readable"
        human = {}
        for key, value in obj.items():
            if key.endswith('Time'):
                value /=  1000 # miliseconds to seconds.
                value = datetime.fromtimestamp(value)
                value = value.astimezone(self.timezone)
                if self.include_date:
                    value = value.strftime('%x %X') # Locale-appropriate Date + Time
                else:
                    value = value.strftime('%X') # Locale-appropriate Time
            if( isinstance(value, dict)
                and _depth <= self.recursion_limit ):
                value = self._time_to_human(value, _depth+1)
            human[key] = value
        return human

    def _extract_expected(self,
                          obj):
        "Extracts expected data to a better formatted prologue."
        prologue = ""

        # Discard the dataAsOfTime for display
        _ = obj.pop('dataAsOfTime', '')

        # Pop out the most intersting stuff into prologue
        if 'match' in obj:
            interesting = ['label',
                           'status']
            for key in interesting:
                prologue += obj['match'].pop(key, '<??>')
                prologue += ' '
            prologue += '\n'

        prologue += 'Event '
        prologue += obj.pop('eventKey', '<???>')
        prologue += '\n'

        # Pop out remaining match details up a level in object
        match = obj.pop('match', {})
        for key, value in match.items():
            newkey  = 'match_'
            newkey += key
            obj[newkey] = value

        return (prologue, obj)

    def _obj_pretty(self, obj):
        "Pretty-print an object"
        return self.pp_for_message.pformat(obj)

    def pretty(self, obj):
        "Prettify the nexus data"
        message = ""

        obj = self._time_to_human(obj)
        prologue, obj = self._extract_expected(obj)

        message += prologue
        message += self._obj_pretty(obj)
        return message
