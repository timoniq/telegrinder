def get_mention_link(user_id: int) -> str:
    return f"tg://user?id={user_id}"


def get_resolve_domain_link(username: str) -> str:
    return f"tg://resolve?domain={username}"


def get_start_bot_link(bot_id: str | int, data: str) -> str:
    if isinstance(bot_id, int):
        return get_mention_link(bot_id) + f"&start={data}"
    return get_resolve_domain_link(bot_id) + f"&start={data}"


def get_start_group_link(bot_id: str | int, data: str) -> str:
    if isinstance(bot_id, int):
        return get_mention_link(bot_id) + f"&startgroup={data}"
    return get_resolve_domain_link(bot_id) + f"&startgroup={data}"


def get_channel_boost_link(channel_id: str | int) -> str:
    if isinstance(channel_id, int):
        return get_mention_link(channel_id) + "&boost"
    return get_resolve_domain_link(channel_id) + "&boost"


def get_invite_chat_link(invite_link: str) -> str:
    return f"tg://join?invite={invite_link}"


__all__ = (
    "get_channel_boost_link",
    "get_invite_chat_link",
    "get_mention_link",
    "get_resolve_domain_link",
    "get_start_bot_link",
    "get_start_group_link",
)
