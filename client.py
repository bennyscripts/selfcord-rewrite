import websocket
import json
import shlex
import asyncio

from .wrapper import Wrapper

from .utils import parse
from .utils import payload
from .utils import exceptions

class Client:
    def __init__(self, command_prefix="!", self_bot=True, debug=False):
        self.ws = None
        self.token = ""
        self.gateway = "wss://gateway.discord.gg/?v=9&encoding=json"
        self.auth_data = payload.generate(self.token)
        self.handlers = []
        self.commands = []
        self.debug = debug
        self.ready_data = None
        self.user = None
        self.connected = False
        self.command_prefix = command_prefix
        self.self_bot = self_bot

    def connect(self, token):
        self.token = token
        Wrapper.set_token(token)
        self.auth_data = payload.generate(self.token)
        self.ws = websocket.WebSocket()
        self.ws.connect(self.gateway)
        self.ws.send(json.dumps(self.auth_data))

    def add_handler(self, event, callback):
        self.handlers.append((event, callback))
        if self.debug: print("[DEBUG] Added handler:", event)

    def add_command(self, name, callback):
        for cmd in self.commands:
            if cmd["name"] == name:
                raise exceptions.DuplicateCommandError(f"A command with the name '{name}' already exists.")


        self.commands.append({"name": name, "callback": callback})
        if self.debug: print("[DEBUG] Added command:", name)

    def on(self, event):
        def decorator(callback):
            self.add_handler(event, callback)
            return callback
        return decorator

    def command(self, name):
        def decorator(callback):
            self.add_command(name, callback)
            return callback
        return decorator

    def run(self, token):
        loop = asyncio.get_event_loop()
        loop.run_until_complete(self.connect(token))
        loop.close()

    async def connect(self, token):
        self.token = token
        Wrapper.set_token(token)
        self.connect(self.token)

        while True:
            try:
                data = self.ws.recv()

                try:
                    json_data = json.loads(data)
                except json.decoder.JSONDecodeError:
                    if self.debug: print("[ERROR] Invalid JSON.")
                    json_data = {}
                    continue

                if "t" in json_data:
                    if str(json_data["t"]).upper() == "READY":
                        Wrapper.set_token(self.token)
                        self.ready_data = json_data
                        self.user = parse.user(self.ready_data["d"]["user"])
                    elif str(json_data["t"]).upper() == "MESSAGE_CREATE" and len(self.commands) > 0:
                        await self.handle_command(json_data)

                    for event, callback in self.handlers:
                        if str(json_data["t"]) == event.upper():
                            if event.upper() == "MESSAGE_CREATE":
                                await callback(parse.message(json_data, self.ready_data))
                            elif event.upper() == "READY":
                                if not self.connected:
                                    self.connected = True
                                    await callback(json_data)
                            else:
                                await callback(json_data)

            except websocket.WebSocketConnectionClosedException:
                if self.debug: print("[ERROR] Lost connection. Attempting to reconnect...")
                self.connect(self.token)
                continue

    async def handle_command(self, msg_data):
        message = parse.message(msg_data, self.ready_data)

        if self.debug:
            print("[DEBUG] Is msg a cmd:", message.content.startswith(self.command_prefix))

        if message.content.startswith(self.command_prefix):
            if self.debug: print("[DEBUG] Command:", message.content)

            if self.self_bot:
                if message.author.id != self.user.id:
                    return

            split = shlex.split(message.content)
            command = split[0][len(self.command_prefix):]
            args = split[1:]

            for handler in self.handlers:
                if handler[0].lower() == "command":
                    await handler[1](command, message)

            for cmd in self.commands:
                if cmd["name"] == command:
                    await cmd["callback"](message, args)
                    break
