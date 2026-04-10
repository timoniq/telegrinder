from msgspex.custom_types import Literal, Option, datetime
from msgspex.model import From, Model, field

type ChatType = Literal["sender", "private", "group", "supergroup", "channel"]


class WebAppChat(Model):
    """Object `WebAppChat`, see the [documentation](https://core.telegram.org/bots/webapps#webappchat).

    This object contains the data of the Mini App chat.
    """

    id: int = field()
    """Unique identifier for this chat. This number may have more than 32
    significant bits and some programming languages may have
    difficulty/silent defects in interpreting it. But it has at most 52
    significant bits, so a signed 64-bit integer or double-precision float
    type are safe for storing this identifier."""

    type: Literal["group", "supergroup", "channel"] = field()
    """Type of chat, can be either `group`, `supergroup` or `channel`."""

    title: str = field()
    """Title of the chat."""

    username: Option[str] = field(default=..., converter=From[str | None])
    """Optional. Username of the chat."""

    photo_url: Option[str] = field(default=..., converter=From[str | None])
    """Optional. URL of the chat’s photo. The photo can be in .jpeg or .svg formats.
    Only returned for Web Apps launched from the attachment menu."""


class WebAppUser(Model):
    """Object `WebAppUser`, see the [documentation](https://core.telegram.org/bots/webapps#webappuser).

    This object contains the data of the Mini App user.
    """

    id: int = field()
    """A unique identifier for the user or bot. This number may have more than 32
    significant bits and some programming languages may have difficulty/silent
    defects in interpreting it. It has at most 52 significant bits, so a 64-bit
    integer or a double-precision float type is safe for storing this identifier."""

    first_name: str = field()
    """First name of the user or bot."""

    is_bot: Option[bool] = field(default=..., converter=From[bool | None])
    """Optional. True, if this user is a bot. Returns in the receiver field only."""

    last_name: Option[str] = field(default=..., converter=From[str | None])
    """Optional. Last name of the user or bot."""

    username: Option[str] = field(default=..., converter=From[str | None])
    """Optional. Username of the user or bot."""

    language_code: Option[str] = field(default=..., converter=From[str | None])
    """Optional. IETF language tag of the user's language. Returns in user field only."""

    is_premium: Option[bool] = field(default=..., converter=From[bool | None])
    """Optional. True, if this user is a Telegram Premium user."""

    added_to_attachment_menu: Option[bool] = field(default=..., converter=From[bool | None])
    """Optional. True, if this user added the bot to the attachment menu."""

    allows_write_to_pm: Option[bool] = field(default=..., converter=From[bool | None])
    """Optional. True, if this user allowed the bot to message them."""

    photo_url: Option[str] = field(default=..., converter=From[str | None])
    """Optional. URL of the user’s profile photo. The photo can be in .jpeg or .svg formats."""


class WebAppInitData(Model):
    """Object `WebAppInitData`, see the [documentation](https://core.telegram.org/bots/webapps#webappinitdata).

    This object contains data that is transferred to the Mini App when it is opened.
    It is empty if the Mini App was launched from a keyboard button or from inline mode.
    """

    auth_date: datetime = field(converter=From[datetime | int])
    """Unix time when the form was opened."""

    hash: str = field()
    """A hash of all passed parameters, which the bot server can use to check their validity."""

    signature: str = field()
    """A signature of all passed parameters (except hash), which the third party
    can use to check their validity."""

    query_id: Option[str] = field(default=..., converter=From[str | None])
    """Optional. A unique identifier for the Mini App session, required for
    sending messages via the answerWebAppQuery method."""

    user: Option[WebAppUser] = field(default=..., converter=From[WebAppUser | None])
    """Optional. An object containing data about the current user."""

    receiver: Option[WebAppUser] = field(default=..., converter=From[WebAppUser | None])
    """Optional. An object containing data about the chat partner of the current
    user in the chat where the bot was launched via the attachment menu. Returned
    only for private chats and only for Mini Apps launched via the attachment menu."""

    chat: Option[WebAppChat] = field(default=..., converter=From[WebAppChat | None])
    """Optional. An object containing data about the chat where the bot was launched
    via the attachment menu. Returned for supergroups, channels and group chats – only
    for Mini Apps launched via the attachment menu."""

    chat_type: Option[ChatType] = field(default=..., converter=From[ChatType | None])
    """Optional. Type of the chat from which the Mini App was opened. Can be either
    `sender` for a private chat with the user opening the link, `private`, `group`,
    `supergroup`, or `channel`. Returned only for Mini Apps launched from direct links."""

    chat_instance: Option[str] = field(default=..., converter=From[str | None])
    """Optional. Global identifier, uniquely corresponding to the chat from which the
    Mini App was opened. Returned only for Mini Apps launched from a direct link."""

    start_param: Option[str] = field(default=..., converter=From[str | None])
    """Optional. The value of the startattach parameter, passed via link. Only
    returned for Mini Apps when launched from the attachment menu via link.

    The value of the `start_param` parameter will also be passed in the GET-parameter
    `tgWebAppStartParam`, so the Mini App can load the correct interface right away.
    """

    can_send_after: Option[int] = field(default=..., converter=From[int | None])
    """Optional. Time in seconds, after which a message can be sent via the answerWebAppQuery method."""


__all__ = ("WebAppChat", "WebAppInitData", "WebAppUser")
