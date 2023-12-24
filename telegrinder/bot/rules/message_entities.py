from telegrinder.types.enums import MessageEntityType

from .abc import Message, MessageRule

Entity = str | MessageEntityType


class HasEntities(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return bool(message.entities)


class MessageEntities(MessageRule, requires=[HasEntities()]):
    def __init__(self, entities: Entity | list[Entity]):
        self.entities = [entities] if not isinstance(entities, list) else entities

    async def check(self, message: Message, ctx: dict) -> bool:
        message_entities = []
        for entity in message.entities.unwrap():
            for entity_type in self.entities:
                if entity_type == entity.type:
                    message_entities.append(entity)

        if not message_entities:
            return False

        ctx["message_entities"] = message_entities
        return True
