from .abc import ABCRule
from telegrinder.modules import json


class CallbackDataEq(ABCRule):
    def __init__(self, value: str):
        self.value = value

    async def check(self, event: dict, ctx: dict) -> bool:
        return event["callback_query"].get("data") == self.value


class CallbackDataJsonEq(ABCRule):
    def __init__(self, d: dict):
        self.d = d

    async def check(self, event: dict, ctx: dict) -> bool:
        if "data" not in event["callback_query"]:
            return False
        try:
            return json.loads(event["callback_query"]["data"]) == self.d
        except:
            return False
