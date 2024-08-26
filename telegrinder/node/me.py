from telegrinder.api.api import API
from telegrinder.node.base import ComposeError, ScalarNode
from telegrinder.node.scope import GLOBAL
from telegrinder.types.objects import User


class Me(ScalarNode, User):
    scope = GLOBAL

    @classmethod
    async def compose(cls, api: API) -> User:
        me = await api.get_me()
        return me.expect(ComposeError("Can't complete get_me request"))


__all__ = ("Me",)
