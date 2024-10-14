from requests import Session

class GroupMe(Session):
    """
    Posts to GroupMe as a Bot
    Notes:
     - Bots are pre-created to post to specific groups.
        - https://dev.groupme.com/bots
     - There is no GroupMe API for posting to specific topic.
        - That's both for Bots and real people API.
    """
    bot_url = 'https://api.groupme.com/v3/bots/post'

    def __init__(self, bot_id):
        super().__init__()
        self.bot_id=bot_id
        return

    def post_message(self, message):
        "Post a Message from Bot"

        data = {"text" : message,
                "bot_id" : self.bot_id}

        result = self.post(GroupMe.bot_url,
                           json=data)
        return result
