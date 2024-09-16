import typing

from telegrinder.bot.dispatch.context import Context
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import MessageEntity

from .message import Message, MessageRule

Entity: typing.TypeAlias = str | MessageEntityType


class HasEntities(MessageRule):
    def check(self, message: Message) -> bool:
        return bool(message.entities)


class MessageEntities(MessageRule, requires=[HasEntities()]):
    def __init__(self, entities: Entity | list[Entity], /) -> None:
        self.entities = [entities] if not isinstance(entities, list) else entities

    def check(self, message: Message, ctx: Context) -> bool:
        message_entities: list[MessageEntity] = []
        for entity in message.entities.unwrap():
            for entity_type in self.entities:
                if entity_type == entity.type:
                    message_entities.append(entity)

        if not message_entities:
            return False

        ctx.message_entities = message_entities
        return True


__all__ = ("HasEntities", "MessageEntities")
