class ParseMode:
    MARKDOWNV2 = "MarkdownV2"
    HTML = "HTML"


def get_mention_link(user_id: int) -> str:
    return f"tg://user?id={user_id}"
