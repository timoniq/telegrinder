import types
import typing
from collections import OrderedDict
from datetime import timedelta
from functools import wraps
from urllib.parse import urlencode

from telegrinder.tools.magic import get_annotations

type DeepLinkFunction[**P] = typing.Callable[P, str]
type NoValue = types.EllipsisType
type Permission = typing.Literal[
    "change_info",
    "post_messages",
    "edit_messages",
    "delete_messages",
    "invite_users",
    "restrict_members",
    "promote_members",
    "pin_messages",
    "manage_topics",
    "manage_video_chats",
    "anonymous",
    "manage_chat",
    "post_stories",
    "edit_stories",
    "delete_stories",
]
type Peer = typing.Literal[
    "users",
    "bots",
    "groups",
    "channels",
]
Parameter = typing.Annotated

NO_VALUE: typing.Final[NoValue] = typing.cast("NoValue", ...)


def deep_link[**P](
    link: str,
    /,
    *,
    no_value_params: set[str] | None = None,
    order_params: set[str] | None = None,
) -> typing.Callable[[DeepLinkFunction[P]], DeepLinkFunction[P]]:
    if not link.startswith("tg://"):
        raise RuntimeError("Invalid deep link format. The link must start with 'tg://'.")

    def inner(func: DeepLinkFunction[P]) -> DeepLinkFunction[P]:
        @wraps(func)
        def wrapper(*_: P.args, **kwargs: P.kwargs) -> str:
            return parse_deep_link(
                link=link,
                params=get_query_params(func, kwargs, order_params),
                no_value_params=no_value_params,
            )

        return wrapper

    return inner


def get_query_params(
    func: DeepLinkFunction[...],
    kwargs: dict[str, typing.Any],
    order_params: set[str] | None = None,
) -> dict[str, typing.Any]:
    annotations = get_annotations(func)
    params = OrderedDict()
    param_names = (
        [*order_params, *(p for p in annotations if p not in order_params)] if order_params else annotations
    )

    for param_name in param_names:
        annotation = annotations[param_name]
        if param_name in kwargs:
            value = kwargs[param_name]
            if typing.get_origin(annotation) is Parameter:
                param_name, validator = get_parameter_metadata(annotation)
                value = validator(value) if validator is not None else value

            params[param_name] = value

    return params


def parse_query_params(
    params: dict[str, typing.Any],
    no_value_params: set[str] | None = None,
    /,
) -> tuple[set[str], dict[str, typing.Any]]:
    no_value_params = no_value_params or set()
    params_: dict[str, typing.Any] = {}

    for key, value in params.items():
        if value in (False, None):
            continue

        if value in (True, NO_VALUE):
            no_value_params.add(key)
            continue
        if isinstance(value, timedelta):
            value = int(value.total_seconds())

        params_[key] = value

    return (no_value_params, params_)


def get_parameter_metadata(
    parameter: typing.Any,
) -> tuple[str, typing.Callable[[typing.Any], typing.Any] | None]:
    meta: tuple[typing.Any, ...] = getattr(parameter, "__metadata__")
    return meta if len(meta) == 2 else (meta[0], None)


def parse_deep_link(
    *,
    link: str,
    params: dict[str, typing.Any],
    no_value_params: set[str] | None = None,
) -> str:
    no_value_params, params = parse_query_params(params, no_value_params)
    query = urlencode(params, encoding="UTF-8") + ("&" if no_value_params else "") + "&".join(no_value_params)
    return f"{link}?{query}"


def validate_permissions(perms: list[Permission] | None, /) -> str | None:
    return None if not perms else "+".join(perms)


def validate_peer(peer: list[Peer] | None, /) -> str | None:
    return None if not peer else "+".join(peer)


@deep_link("tg://resolve")
def tg_public_username_link(
    *,
    username: Parameter[str, "domain"],
    draft_text: Parameter[str | None, "text"] = None,
    open_profile: Parameter[bool, "profile"] = False,
) -> str:
    """Used to link to public `users`, `groups` and `channels`.

    :param username: Username.
    :param draft_text: Optional. UTF-8 text to pre-enter into the text input bar, if the user can write in the chat.
    :param open_profile: Optional. If set, clicking on this link should open the destination peer's profile page, not the chat view.
    """
    ...


@deep_link("tg://user")
def tg_mention_link(*, user_id: Parameter[int, "id"]) -> str:
    """ID links are merely an abstraction offered by the `Bot API` to simplify construction of
    `inputMessageEntityMentionName` and `inputKeyboardButtonUserProfile` constructors, and should be
    ignored by normal clients.

    :param user_id: User ID.
    """
    ...


@deep_link("tg://openmessage")
def tg_open_message_link(
    *,
    chat_id: int | None = None,
    user_id: int | None = None,
    message_id: int | None = None,
) -> str: ...


@deep_link("tg://emoji")
def tg_emoji_link(*, emoji_id: Parameter[int, "id"]) -> str:
    """Emoji links are merely an abstraction offered by the `Bot API` to simplify construction of
    `messageEntityCustomEmoji` constructors, and should be ignored by normal clients.

    :param emoji_id: Custom emoji ID.
    """
    ...


@deep_link("tg://addemoji")
def tg_emoji_stickerset_link(*, short_name: Parameter[str, "set"]) -> str:
    """Used to import custom emoji stickersets.

    :param short_name: Stickerset short name, used when installing stickers.
    """
    ...


@deep_link("tg://resolve")
def tg_story_link(
    *,
    username: Parameter[str, "domain"],
    story_id: Parameter[int, "story"],
) -> str:
    """Used to link to a Telegram Story.

    :param username: Username of the user or channel that posted the story.
    :param story_id: ID of the Telegram Story.
    """
    ...


@deep_link("tg://join")
def tg_chat_invite_link(*, invite_hash: Parameter[str, "invite"]) -> str:
    """Used to invite users to private `groups` and `channels`.

    :param invite_hash: Invite hash.
    """
    ...


@deep_link("tg://addlist")
def tg_chat_folder_link(*, slug: str) -> str:
    """Used to add chat folders.

    :param slug: Folder slug.
    """
    ...


@deep_link("tg://resolve")
def tg_public_message_link(
    *,
    dialog: Parameter[str, "domain"],
    message_id: Parameter[int, "post"],
    single: bool = False,
    thread_id: Parameter[int | None, "thread"] = None,
    comment: str | None = None,
    timestamp: Parameter[timedelta | None, "t"] = None,
) -> str:
    """Used to link to specific messages in public or private `groups` and `channels`.

    :param dialog: Dialog username.
    :param message_id: Message ID.
    :param single: Optional. For albums/grouped media, if set indicates that this is a link to a specific media in the album; otherwise, it is a link to the entire album.
    :param thread_id: Optional. For message threads, contains the thread ID.
    :param comment: Optional. For channel comments, username will contain the channel username, id will contain the message ID of the channel message that started the comment section and this field will contain the message ID of the comment in the discussion group.
    :param timestamp: Optional. Timestamp at which to start playing the media file present in the body or in the webpage preview of the message.
    """
    ...


@deep_link("tg://privatepost")
def tg_private_message_link(
    *,
    channel: str,
    message_id: Parameter[int, "post"],
    single: bool = False,
    thread_id: Parameter[int | None, "thread"] = None,
    comment: str | None = None,
    timestamp: Parameter[timedelta | None, "t"] = None,
) -> str:
    """Used to link to specific messages in public or private `groups` and `channels`.

    :param channel: Channel or supergroup ID.
    :param post: Message ID.
    :param single: Optional. For albums/grouped media, if set indicates that this is a link to a specific media in the album; otherwise, it is a link to the entire album.
    :param thread: Optional. For message threads, contains the thread ID.
    :param comment: Optional. For channel comments, username will contain the channel username, id will contain the message ID of the channel message that started the comment section and this field will contain the message ID of the comment in the discussion group.
    :param t: Optional. Timestamp at which to start playing the media file present in the body or in the webpage preview of the message.
    """
    ...


@deep_link("tg://msg_url")
def tg_share_link(*, url: str, text: str | None = None) -> str:
    """Used to share a prepared message and URL into a chosen chat's text field.

    These links should be handled as follows:
    * Open a dialog selection prompt
    * After selection: validate, trim and enter the URL at the beginning of the text field
    * Append a newline to the text field
    * Append and select the `text`, if present

    :param url: URL to share (`urlencoded`).
    :param text: Optional. Text to prepend to the URL.
    """
    ...


@deep_link("tg://boost")
def tg_public_channel_boost_link(*, channel_username: Parameter[str, "domain"]) -> str:
    """Used by users to boost public channels, granting them the ability to post stories and further perks.

    :param channel_username: Channel username.
    """
    ...


@deep_link("tg://boost")
def tg_private_channel_boost_link(*, channel_id: Parameter[int, "channel"]) -> str:
    """Used by users to boost private channels, granting them the ability to post stories and further perks.

    :param channel_id: Channel ID.
    """
    ...


@deep_link("tg://invoice")
def tg_invoice_link(*, slug: str) -> str:
    """Used to initiate payment of an invoice, generated using `payments.exportedInvoice`.

    :param slug: The invoice slug to be used during payment.
    """
    ...


@deep_link("tg://setlanguage")
def tg_language_pack_link(
    *,
    lang_pack: Parameter[str | None, "lang"] = None,
) -> str:
    """Used to import custom language packs using `langpack.getLangPack`.

    :param lang_pack: Optional. Name of language pack.
    """
    ...


@deep_link("tg://premium_multigift")
def tg_premium_multigift_link(*, ref: str) -> str:
    """Used to bring the user to the screen used for gifting `Telegram Premium` subscriptions to friends,
    see here for more info on gifting `Telegram Premium` to multiple users.

    This link is used to invite users to gift `Premium` subscription to other users, see here for the different
    link type containing the actual giftcodes that can be used to import a gifted `Telegram Premium` subscription.

    :param ref: Used by official apps for analytics using `help.saveAppLog`.
    """
    ...


@deep_link("tg://premium_offer")
def tg_premium_offer_link(*, ref: str | None = None) -> str:
    """Used by official apps to show the `Telegram Premium` subscription page.

    :param ref: Optional. Used by official apps for analytics using `help.saveAppLog`.
    """
    ...


@deep_link("tg://resolve")
def tg_bot_start_link(
    *,
    bot_username: Parameter[str, "domain"],
    parameter: Parameter[str | None, "start"] = None,
) -> str:
    """Used to link to bots.

    :param bot_username: Bot username.
    :param parameter: Optional. Start parameter, up to 64 `base64url` characters: if provided and the `bot_username` is indeed a bot, \
    the text input bar should be replaced with a `Start` button (even if the user has already started the bot) that should invoke \
    `messages.startBot` with the appropriate `parameter` once clicked. Note that if the `bot_username` is equal to the `premium_bot_username` \
    configuration value, clicking on this link should immediately invoke `messages.startBot` with the appropriate `parameter`.
    """
    ...


@deep_link("tg://resolve")
def tg_bot_startgroup_link(
    *,
    bot_username: Parameter[str, "domain"],
    parameter: Parameter[str | NoValue, "startgroup"] = NO_VALUE,
    permissions: Parameter[list[Permission] | None, "admin", validate_permissions] = None,
) -> str:
    """Used to add bots to groups.
    First of all, check that the `<bot_username>` indeed links to a bot.

    Then, for group links:

    If the `admin` parameter is not provided:
        - Bring up a dialog selection of groups where the user can add members
        - Add the bot to the group
        - If a `parameter` is provided, invoke `messages.startBot` with the appropriate `parameter`

    If the admin parameter is provided:
        - Bring up a dialog selection of groups where the user can add/edit admins
        - If the bot is already an admin of the group, combine existing admin rights with the admin rights in admin
        - Add the bot as admin/modify admin permissions to the new rights
        - If a parameter is provided, invoke `messages.startBot` with the appropriate `parameter`

    :param bot_username: Bot username.
    :param parameter: Optional. Start parameter, only for group links, up to 64 `base64url` characters: if provided and the `bot_username` is indeed a bot, \
    `messages.startBot` with the appropriate parameter should be invoked after adding the bot to the group.
    :param permissions: Optional. A combination of the following identifiers separated by `+`, each corresponding to the appropriate flag in the `chatAdminRights` constructor.
    """
    ...


@deep_link("tg://resolve", no_value_params={"startchannel"})
def tg_bot_startchannel_link(
    *,
    bot_username: Parameter[str, "domain"],
    permissions: Parameter[list[Permission], "admin", validate_permissions],
) -> str:
    """Used to add bots to channels.
    First of all, check that the `<bot_username>` indeed links to a bot.

    For channel links:
    - Bring up a dialog selection of channels where the user can add/edit admins
    - If the bot is already an admin of the channel, combine existing admin rights with the admin rights in admin
    - Add the bot as admin/modify admin permissions to the new rights

    :param bot_username: Bot username.
    :param permissions: A combination of the following identifiers separated by `+`, each corresponding to the \
    appropriate flag in the `chatAdminRights` constructor.
    """
    ...


@deep_link("tg://resolve")
def tg_main_mini_app_link(
    *,
    bot_username: Parameter[str, "domain"],
    parameter: Parameter[str | NoValue, "startapp"] = NO_VALUE,
    mode: typing.Literal["compact"] | None = None,
) -> str:
    """Used to open `Main Mini Apps`.

    If the specified bot does not have a configured `Main` Mini App (i.e. the user.bot_has_main_app flag will not be set),
    fall back to the behavior of username links.

    The main mini app should be opened using `messages.requestMainWebView`.

    :param bot_username: Bot username.
    :param parameter: Optional. If provided, should be passed to `messages.requestMainWebView.start_param`.
    :param mode: Optional. If equal to `compact`, the `messages.requestMainWebView.compact` flag must be set.
    """
    ...


@deep_link("tg://resolve")
def tg_direct_mini_app_link(
    *,
    bot_username: Parameter[str, "domain"],
    short_name: Parameter[str, "appname"],
    parameter: Parameter[str | NoValue, "startapp"] = NO_VALUE,
    mode: typing.Literal["compact"] | None = None,
) -> str:
    """Used to share `Direct` link Mini apps.

    These links are different from bot attachment menu deep links, because they don't require the user to install
    an attachment menu, and a single bot can offer multiple named mini apps, distinguished by their `short_name`.

    These links should be handled as specified in the direct link Mini Apps documentation.

    :param bot_username: Username of the bot that owns the game.
    :param short_name: Mini app short name, to pass to `inputBotAppShortName.short_name` when invoking `messages.getBotApp`.
    :param parameter: Optional. To pass to `messages.requestAppWebView.start_param`.
    :param mode: Optional. If equal to `compact`, the `messages.requestAppWebView.compact` flag must be set.
    """
    ...


@deep_link("tg://resolve")
def tg_bot_attach_open_current_chat(
    *,
    bot_username: Parameter[str, "domain"],
    parameter: Parameter[str | NoValue, "startattach"] = NO_VALUE,
) -> str:
    """After installing the attachment/side menu entry globally, opens the associated mini app using
    `messages.requestWebView` in the currently open chat, by passing it to the peer parameter of `messages.requestWebView`.

    If the current chat is not supported by the `attachMenuBot.peer_types` field:

    - If the user has just installed the attachment menu in the previous step, notify the user that the attachment menu was installed successfully.
    - Otherwise, notify the user that the attachment menu webapp can't be opened in the specified chat.

    :param bot_username: Username of the bot that owns the attachment/side menu entry.
    :param parameter: Optional. If provided, should be passed to `messages.requestWebView.start_param`.
    """
    ...


@deep_link("tg://resolve")
def tg_bot_attach_open_specific_chat(
    *,
    username: Parameter[str, "domain"],
    phone_number: Parameter[str, "phone"],
    bot_username: Parameter[str, "attach"],
    parameter: Parameter[str | NoValue, "startattach"] = NO_VALUE,
) -> str:
    """After installing the `attachment/side` menu entry globally, opens the associated mini app using
    `messages.requestWebView` in a specific chat (passed to the peer parameter of `messages.requestWebView`).

    If the specified chat is not supported by the attachMenuBot.peer_types field:

    - If the user has just installed the attachment menu in the previous step, notify the user that the attachment menu was installed successfully.
    - Otherwise, notify the user that the attachment menu webapp can't be opened in the specified chat.
    """
    ...


@deep_link("tg://resolve")
def tg_bot_attach_open_any_chat(
    *,
    bot_username: Parameter[str, "domain"],
    parameter: Parameter[str | NoValue, "startattach"] = NO_VALUE,
    peer: Parameter[list[Peer] | None, "choose", validate_peer] = None,
) -> str:
    """After installing the `attachment/side` menu entry globally, opens a dialog selection form that will open the attachment menu
    mini app using `messages.requestWebView` in a specific chat (pass it to the peer parameter of `messages.requestWebView`).

    :param bot_username: Username of the bot that owns the `attachment/side` menu.
    :param parameter: Optional. If provided, should be passed to `messages.requestWebView.start_param`.
    :param peer: Optional. A combination of `users`, `bots`, `groups`, `channels` separated by `+`: indicates the dialog types to show in \
    the dialog selection popup: must be intersected with the dialog types contained in the `attachMenuBot.peer_types` field before use.
    """
    ...


__all__ = (
    "tg_bot_attach_open_any_chat",
    "tg_bot_attach_open_current_chat",
    "tg_bot_attach_open_specific_chat",
    "tg_bot_start_link",
    "tg_bot_startchannel_link",
    "tg_bot_startgroup_link",
    "tg_chat_folder_link",
    "tg_chat_invite_link",
    "tg_direct_mini_app_link",
    "tg_emoji_link",
    "tg_emoji_stickerset_link",
    "tg_invoice_link",
    "tg_language_pack_link",
    "tg_main_mini_app_link",
    "tg_mention_link",
    "tg_open_message_link",
    "tg_premium_multigift_link",
    "tg_premium_offer_link",
    "tg_private_channel_boost_link",
    "tg_private_message_link",
    "tg_public_channel_boost_link",
    "tg_public_message_link",
    "tg_public_username_link",
    "tg_share_link",
    "tg_story_link",
)
