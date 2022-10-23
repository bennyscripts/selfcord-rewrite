from .get import guild as get_guild
from .get import channel as get_channel

from ..types import message as msg
from ..types import user as usr

def user(user_data):
    return usr.User(user_data["id"], user_data["username"], user_data["discriminator"], user_data["avatar"])

def message(msg_data, ready_data):
    data = msg_data["d"]
    _id = data["id"]
    content = data["content"]
    timestamp = data["timestamp"]
    author = user(data["author"])
    channel_id = data.get("channel_id", None)
    guild_id = data.get("guild_id", None)

    guild = get_guild(guild_id, ready_data) if guild_id is not None else None
    if channel_id is not None:
        channel = get_channel(channel_id, guild_id, ready_data)
    else:
        channel = None

    return msg.Message(_id, content, timestamp, author, channel, channel_id, guild, guild_id)