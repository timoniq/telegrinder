from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node

from telegrinder.api.api import API
from telegrinder.node.scope import global_node
from telegrinder.types.objects import User


@global_node
@scalar_node
class Me:
    @classmethod
    async def __compose__(cls, api: API) -> User:
        me = await api.get_me()
        return me.expect(NodeError("Can't complete api.get_me() request."))


@global_node
@scalar_node
class BotUsername:
    @classmethod
    def __compose__(cls, me: Me) -> str:
        return me.username.unwrap()


__all__ = ("BotUsername", "Me")
