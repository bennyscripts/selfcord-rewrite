import httpx

client = httpx.Client()
user_token = ""
base_url = "https://discordapp.com/api/v9"

class Wrapper:
    def set_token(self):
        global user_token
        user_token = self

    def get_token():
        global user_token
        return user_token

    def send_request(self, url, headers=None, data=None):
        if headers is None:
            headers = {}
        if data is None:
            data = {}
        return client.request(self, url, headers=headers, data=data)

    def send_discord_request(self, endpoint, headers={}, data={}):
        global user_token

        headers["Authorization"] = f"{user_token}"
        headers["Content-Type"] = "application/json"

        return client.request(self, base_url + endpoint, headers=headers, data=data)
