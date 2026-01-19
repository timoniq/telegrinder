from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.types.objects import Chat, MessageOriginChannel

type MessageChannelPostDiscussion = MessageOriginChannel


@scalar_node
class ChannelPostDiscussion:
    @classmethod
    def __compose__(cls, message: MessageCute) -> MessageChannelPostDiscussion:
        forward_origin = message.forward_origin.expect(NodeError("Message has no forward origin."))
        return forward_origin.only(MessageOriginChannel).expect(NodeError("Message forward origin is not a channel."))


@scalar_node
class ChannelPostDiscussionId:
    @classmethod
    def __compose__(cls, discussion: ChannelPostDiscussion) -> int:
        return discussion.message_id


@scalar_node
class ChannelPostDiscussionChat:
    @classmethod
    def __compose__(cls, discussion: ChannelPostDiscussion) -> Chat:
        return discussion.chat


@scalar_node
class ChannelPostDiscussionChatId:
    @classmethod
    def __compose__(cls, discussion_chat: ChannelPostDiscussionChat) -> int:
        return discussion_chat.id


@scalar_node
class ChannelPostDiscussionPostAuthor:
    @classmethod
    def __compose__(cls, discussion: ChannelPostDiscussion) -> str:
        return discussion.author_signature.expect(NodeError("Discussion has no signature of the post author."))


__all__ = (
    "ChannelPostDiscussion",
    "ChannelPostDiscussionChat",
    "ChannelPostDiscussionChatId",
    "ChannelPostDiscussionId",
    "ChannelPostDiscussionPostAuthor",
)
