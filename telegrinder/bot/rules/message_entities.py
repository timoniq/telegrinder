import typing

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.enums import MessageEntityType
from telegrinder.types.objects import MessageEntity

type Entity = str | MessageEntityType

Message: typing.TypeAlias = MessageCute


class HasEntities(ABCRule):
    def check(self, message: Message) -> bool:
        return bool(message.entities)


class MessageEntities(ABCRule, requires=[HasEntities()]):
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
