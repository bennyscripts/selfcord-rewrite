import json
import asyncio

from ..wrapper import Wrapper

class Message:
    def __init__(self, _id, content, timestamp, author, channel, channel_id, guild, guild_id, edited_timestamp=""):
        self.id = _id
        self.content = content
        self.timestamp = timestamp
        self.author = author
        # TODO: add support for dm channels
        self.channel = channel
        self.channel_id = channel_id
        self.guild = guild
        self.guild_id = guild_id
        self.edited_timestamp = edited_timestamp

    async def delete(self, delay=0):
        # TODO: prevent delay from pausing the program
        if delay > 0:
            await asyncio.sleep(delay)

        try:
            return Wrapper.send_discord_request("DELETE", f"/channels/{self.channel_id}/messages/{self.id}")
        except Exception as e:
            print(e)
            return None

    def edit(self, content):
        try:
            resp = Wrapper.send_discord_request("PATCH", f"/channels/{self.channel_id}/messages/{self.id}", data=json.dumps({"content": str(content)}))
            return Message(resp.json()["id"], resp.json()["content"], self.timestamp, self.author, self.channel, self.channel_id, self.guild, self.guild_id, edited_timestamp=resp.json()["edited_timestamp"])
        except Exception as e:
            print(e)
            return None