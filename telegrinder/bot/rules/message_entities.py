from .abc import Message, MessageRule
from telegrinder.types.enums import MessageEntityType

EntityType = str | MessageEntityType


class HasEntities(MessageRule):
    async def check(self, message: Message, _) -> bool:
        return bool(message.entities)


class MessageEntitiesRule(MessageRule, require=[HasEntities()]):
    def __init__(self, entities: EntityType | list[EntityType]):
        self.entities = [entities] if not isinstance(entities, list) else entities

    async def check(self, message: Message, ctx: dict) -> bool:
        message_entities = []
        for entity in message.entities:
            for entity_type in self.entities:
                if entity_type == entity.type:
                    message_entities.append(entity)

        if not message_entities:
            return False

        ctx["message_entities"] = message_entities
        return True
