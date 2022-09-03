import json

from ..wrapper import Wrapper

class Channel:
    def __init__(self, _id, name, topic, nsfw, guild):
        self.id = _id
        self.name = name
        self.topic = topic
        self.nsfw = nsfw
        self.guild = guild

    def send(self, content):
        try:
            return Wrapper.send_discord_request("POST", f"/channels/{self.id}/messages", data=json.dumps({"content": str(content)}))
        except Exception as e:
            print(e)
            return None