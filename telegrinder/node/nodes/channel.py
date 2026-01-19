from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.types.enums import ChatType
from telegrinder.types.objects import Chat, MessageOriginChannel

type MessageChannelPostDiscussion = MessageOriginChannel
type MessageChannelPost = MessageCute


@scalar_node
class ChannelPost:
    @classmethod
    def __compose__(cls, message: MessageCute) -> MessageChannelPost:
        if message.chat.type != ChatType.CHANNEL:
            raise NodeError("Message is not a channel post.")
        return message


@scalar_node
class Channel:
    @classmethod
    def __compose__(cls, channel_post: ChannelPost) -> Chat:
        return channel_post.chat


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
    "Channel",
    "ChannelPost",
    "ChannelPostDiscussion",
    "ChannelPostDiscussionChat",
    "ChannelPostDiscussionChatId",
    "ChannelPostDiscussionId",
    "ChannelPostDiscussionPostAuthor",
)
