def get_mention_link(user_id: int) -> str:
    return f"tg://user?id={user_id}"


def get_resolve_domain_link(username: str) -> str:
    return f"tg://resolve?domain={username}"


def get_start_bot_link(bot_username: str, data: str) -> str:
    return get_resolve_domain_link(bot_username) + f"&start={data}"


def get_start_group_link(bot_username: str, data: str) -> str:
    return get_resolve_domain_link(bot_username) + f"&startgroup={data}"


def get_channel_boost_link(channel_username: str) -> str:
    return get_resolve_domain_link(channel_username) + "&boost"


def get_invite_chat_link(invite_link: str) -> str:
    return f"tg://join?invite={invite_link}"


def user_open_message_link(user_id: int, message: str | None = None) -> str:
    return f"tg://openmessage?user_id={user_id}" + (
        "" if not message else f"&msg?text={message}"
    )


__all__ = (
    "get_channel_boost_link",
    "get_invite_chat_link",
    "get_mention_link",
    "get_resolve_domain_link",
    "get_start_bot_link",
    "get_start_group_link",
    "user_open_message_link",
)
