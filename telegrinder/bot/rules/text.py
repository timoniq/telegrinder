from .abc import ABCMessageRule, Message
import typing


class Text(ABCMessageRule):
    def __init__(
        self, texts: typing.Union[str, typing.List[str]], ignore_case: bool = False
    ):
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts
        self.ignore_case = ignore_case

    async def check(self, message: Message, ctx: dict) -> bool:
        if self.ignore_case:
            return message.text.lower() in list(map(str.lower, self.texts))
        return message.text in self.texts
