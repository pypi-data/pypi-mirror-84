import requests
import json


class Botlists:
    def __init__(self, api_key: str):
        if type(api_key) is not str:
            raise ValueError(f"please enter a string as param, you entered {type(api_key)}")
        self.url = 'https://botlists.com/api/bot'
        self.api_key = api_key

    def get(self):
        r = requests.get(self.url, headers={"token": self.api_key})
        return r.content

    def count(self, server_count: int):
        if type(server_count) is not int:
            raise ValueError(f"please enter a number as param, you entered {type(server_count)}")
        body = {"guild_count": server_count}
        r = requests.post(self.url, data=json.dumps(body), headers={"token": self.api_key, "Content-Type": "application/json"})
        return r.content
