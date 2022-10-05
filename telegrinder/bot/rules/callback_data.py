from .abc import ABCRule
from telegrinder.modules import json
from telegrinder.types import Update


class CallbackDataEq(ABCRule):
    def __init__(self, value: str):
        self.value = value

    async def check(self, event: Update, ctx: dict) -> bool:
        return event.callback_query.data == self.value


class CallbackDataJsonEq(ABCRule):
    def __init__(self, d: dict):
        self.d = d

    async def check(self, event: Update, ctx: dict) -> bool:
        if not event.callback_query.data:
            return False
        try:
            # todo: use msgspec
            return json.loads(event.callback_query.data) == self.d
        except:
            return False
