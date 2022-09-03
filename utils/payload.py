def generate(token):
    return {
            "op": 2,
            "d": {
                "token": token,
                "properties": {
                    "$os": "linux",
                    "$browser": "discord.py",
                    "$device": "discord.py"
                },
                "compress": False,
                "large_threshold": 250,
                "shard": [0, 1]
            }
        }