from ..types import guild as _guild
from ..types import channel as _channel

def guild(id, ready_data):
    for guild_ in ready_data["d"]["guilds"]:
        if guild_["id"] == id:
            return _guild.Guild(guild_["id"], guild_["name"], guild_["description"], guild_["owner_id"], guild_["icon"], guild_["banner"], guild_["member_count"])
    return None

def channel(id, guild_id, ready_data):
    for guild_ in ready_data["d"]["guilds"]:
        guild_obj = guild(guild_["id"], ready_data)
        if guild_["id"] == guild_id:
            for channel in guild_["channels"]:
                if channel["id"] == id:
                    return _channel.Channel(channel["id"], channel["name"], channel["topic"], channel.get("nsfw", False), guild_obj)
    return None