from nodnod.error import NodeError
from nodnod.interface.scalar import scalar_node
from nodnod.node import Scalar

from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.types.enums import ChatType
from telegrinder.types.objects import Chat, MessageOriginChannel

type MessageChannelPost = MessageOriginChannel
type Post = MessageCute
type PostId = int


@scalar_node
class ChatMessageChannelPost:
    @classmethod
    def __compose__(cls, message: MessageCute) -> MessageChannelPost:
        forward_origin = message.forward_origin.expect(NodeError("Message has no forward origin."))
        return forward_origin.only(MessageOriginChannel).expect(NodeError("Message forward origin is not a channel."))


@scalar_node
class ChatMessageChannelPostId:
    @classmethod
    def __compose__(cls, message_channel_post: ChatMessageChannelPost) -> PostId:
        return message_channel_post.message_id


@scalar_node
class ChatMessageChannelPostChannel:
    @classmethod
    def __compose__(cls, message_channel_post: ChatMessageChannelPost) -> Channel:
        return message_channel_post.chat


@scalar_node
class ChatMessageChannelPostChannelId:
    @classmethod
    def __compose__(cls, message_channel_post: ChatMessageChannelPost) -> ChannelId:
        return message_channel_post.chat.id


@scalar_node
class ChatMessageChannelPostAuthor:
    @classmethod
    def __compose__(cls, message_channel_post: ChatMessageChannelPost) -> str:
        return message_channel_post.author_signature.expect(
            NodeError("Discussion has no signature of the post author."),
        )


@scalar_node
class ChannelPostNode:
    @classmethod
    def __compose__(cls, message: MessageCute) -> ChannelPost:
        if message.chat.type != ChatType.CHANNEL:
            raise NodeError("Message is not a channel post.")
        return message


@scalar_node
class ChannelPostId:
    @classmethod
    def __compose__(cls, channel_post: ChannelPostNode) -> PostId:
        return channel_post.message_id


@scalar_node
class ChannelNode:
    @classmethod
    def __compose__(cls, channel_post: ChannelPostNode) -> Channel:
        return channel_post.chat


@scalar_node
class ChannelIdNode:
    @classmethod
    def __compose__(cls, channel_post: ChannelPostNode) -> ChannelId:
        return channel_post.chat.id


type Channel = Scalar[Chat, ChannelNode]
type ChannelId = Scalar[int, ChannelIdNode]
type ChannelPost = Scalar[MessageCute, ChannelPostNode]


__all__ = (
    "Channel",
    "ChannelId",
    "ChannelPost",
    "ChannelPostId",
    "ChatMessageChannelPost",
    "ChatMessageChannelPostAuthor",
    "ChatMessageChannelPostChannel",
    "ChatMessageChannelPostChannelId",
    "ChatMessageChannelPostId",
)
