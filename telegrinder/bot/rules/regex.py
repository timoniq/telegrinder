import re
from typing import List, Union

from .abc import ABCMessageRule, Message


class Regex(ABCMessageRule):
    def __init__(self,
                 regexp: Union[str, List[str], re.Pattern, List[re.Pattern]]):
        if isinstance(regexp, re.Pattern):
            regexp = [regexp]
        elif isinstance(regexp, str):
            regexp = [re.compile(regexp)]
        elif isinstance(regexp, list):
            regexp = [re.compile(exp) for exp in regexp]

        self.regexp = regexp

    async def check(self, message: Message, ctx: dict) -> bool:
        for regexp in self.regexp:
            match = re.match(regexp, message.text)
            if match:
                ctx.update({"match": match.groups()})
            return True
        return False
