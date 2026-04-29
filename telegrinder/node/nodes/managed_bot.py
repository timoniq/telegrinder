import telegrinder.types.objects
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.node import NodeError, scalar_node

type Bot = telegrinder.types.objects.User
type BotId = int
type BotName = str
type BotUsername = str


@scalar_node
class ManagedBotCreated:
    @classmethod
    def __compose__(cls, message: MessageCute) -> telegrinder.types.objects.ManagedBotCreated:
        return message.managed_bot_created.expect(NodeError("Message has no managed bot created."))


@scalar_node
class ManagedBotCreatedBot:
    @classmethod
    def __compose__(cls, managed_bot_created: ManagedBotCreated) -> Bot:
        return managed_bot_created.bot


@scalar_node
class ManagedBotCreatedBotId:
    @classmethod
    def __compose__(cls, managed_bot_created_bot: ManagedBotCreatedBot) -> BotId:
        return managed_bot_created_bot.id


@scalar_node
class ManagedBotCreatedBotName:
    @classmethod
    def __compose__(cls, managed_bot_created_bot: ManagedBotCreatedBot) -> BotUsername:
        return managed_bot_created_bot.full_name


@scalar_node
class ManagedBotCreatedBotUsername:
    @classmethod
    def __compose__(cls, managed_bot_created_bot: ManagedBotCreatedBot) -> BotUsername:
        return managed_bot_created_bot.username.unwrap()


__all__ = (
    "ManagedBotCreated",
    "ManagedBotCreatedBot",
    "ManagedBotCreatedBotId",
    "ManagedBotCreatedBotName",
    "ManagedBotCreatedBotUsername",
)
