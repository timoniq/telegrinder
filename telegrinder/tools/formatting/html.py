from .abc import ABCFormatter
import typing
from telegrinder.tools.parse_mode import ParseMode

QUOT_MARK = '"'


def wrap_tag(
    tag_name: str, content: str, data: typing.Optional[dict] = None
) -> "HTMLFormatter":
    s = "<" + tag_name
    if data:
        for k, v in data.items():
            s += f" {k}={v}"
    s += ">" + content + "</" + tag_name + ">"
    return HTMLFormatter(s)


class HTMLFormatter(ABCFormatter):
    PARSE_MODE = ParseMode.HTML

    def escape(self) -> "HTMLFormatter":
        return self.replace("&", "&amp;").replace(">", "&gt;").replace("<", "&lt;")

    def bold(self) -> "HTMLFormatter":
        return wrap_tag("b", self)

    def italic(self) -> "HTMLFormatter":
        return wrap_tag("i", self)

    def underline(self) -> "HTMLFormatter":
        return wrap_tag("u", self)

    def strike(self) -> "HTMLFormatter":
        return wrap_tag("s", self)
    
    def spoiler(self) -> "HTMLFormatter":
        return wrap_tag("tg-spoiler", self)

    def link(self, href: str) -> "HTMLFormatter":
        return wrap_tag(
            "a",
            self.escape(),
            data={"href": QUOT_MARK + HTMLFormatter(href).escape() + QUOT_MARK},
        )

    def code_block(self) -> "HTMLFormatter":
        return wrap_tag("pre", self.escape())

    def code_block_with_lang(self, lang: str) -> "HTMLFormatter":
        return wrap_tag(
            "pre", wrap_tag("code", self.escape(), data={"class": f"language-{lang}"})
        )

    def code_inline(self) -> "HTMLFormatter":
        return wrap_tag("code", self.escape())
