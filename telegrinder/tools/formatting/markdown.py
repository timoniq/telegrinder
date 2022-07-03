from .abc import ABCFormatter
import typing
from telegrinder.tools.parse_mode import ParseMode

FMT_CHARS = "\\`*_{}[]()#+-!"


def wrap_md(wrapper: str, s: str) -> "MarkdownFormatter":
    return MarkdownFormatter(wrapper + s + wrapper)


class MarkdownFormatter(ABCFormatter):
    PARSE_MODE = ParseMode.MARKDOWNV2

    def escape(self) -> "MarkdownFormatter":
        ns = ""
        for c in self:
            if c in FMT_CHARS:
                ns += "\\"
            ns += c
        ns = ns.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
        return MarkdownFormatter(ns)

    def escape_code(self) -> "MarkdownFormatter":
        return self.replace("\\", "\\\\").replace("`", "\\`")

    def escape_link(self) -> "MarkdownFormatter":
        return self.replace("`", "\\`").replace(")", "\\)")

    def bold(self) -> "MarkdownFormatter":
        return wrap_md("*", self)

    def italic(self) -> "MarkdownFormatter":
        return wrap_md("_", self)

    def underline(self) -> "MarkdownFormatter":
        return wrap_md("__", self)

    def strike(self) -> "MarkdownFormatter":
        return wrap_md("~", self)

    def link(self, href: str) -> "MarkdownFormatter":
        return MarkdownFormatter(
            f"[{self.escape()}]({MarkdownFormatter(href).escape_link()})"
        )

    def code_block(self) -> "MarkdownFormatter":
        return MarkdownFormatter(f"```\n{self.escape_code()}\n```")

    def code_block_with_lang(self, lang: str) -> "MarkdownFormatter":
        return MarkdownFormatter(
            f"```{MarkdownFormatter(lang).escape()}\n{self.escape_code()}\n```"
        )

    def code_inline(self) -> "MarkdownFormatter":
        return MarkdownFormatter(f"`{self.escape_code()}`")
