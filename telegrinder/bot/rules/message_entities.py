from .abc import Message, MessageRule
from telegrinder.types.enums import MessageEntityType


class HasEntities(MessageRule):
    async def check(self, message: Message, _) -> bool:
        return bool(message.entities)


class MessageEntitiesRule(MessageRule, require=[HasEntities()]):
    def __init__(self, *entities: str | MessageEntityType):
        if not entities:
            raise ValueError("entities is required.")
        self.entities = entities

    async def check(self, message: Message, ctx: dict) -> bool:
        message_entities = []
        for entity in message.entities:
            for entity_type in self.entities:
                if entity.type in entity_type:
                    message_entities.append(entity)

        if not message_entities:
            return False

        ctx["message_entities"] = message_entities
        return True
