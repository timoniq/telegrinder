from telegrinder.api.api import API
from telegrinder.node.base import ComposeError, scalar_node
from telegrinder.node.scope import global_node
from telegrinder.types.objects import User


@scalar_node
@global_node
class Me:
    @classmethod
    async def compose(cls, api: API) -> User:
        me = await api.get_me()
        return me.expect(ComposeError("Can't complete api.get_me() request."))


__all__ = ("Me",)
