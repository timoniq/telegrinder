from .abc import ABC, MessageRule, Message, ABCTranslatedRule
from ...tools.i18n.constants import I18N_KWARG_NAME


class HasText(MessageRule):
    async def check(self, message: Message, ctx: dict) -> bool:
        return bool(message.text)


class TextMessageRule(MessageRule, ABC, require=[HasText()]):
    pass


class Text(TextMessageRule):
    def __init__(self, texts: str | list[str], ignore_case: bool = False):
        if not isinstance(texts, list):
            texts = [texts]
        self.texts = texts if not ignore_case else list(map(str.lower, texts))
        self.ignore_case = ignore_case

    def check_text(self, text: str, override_texts: list[str] | None = None) -> bool:
        texts = override_texts or self.texts
        return (
            text if not self.ignore_case else text.lower()
        ) in texts

    async def check(self, message: Message, ctx: dict) -> bool:
        return self.check_text(message.text)

    def translate(self) -> "TranslatedText":
        return TranslatedText(inner_rule=self)


class TranslatedText(ABCTranslatedRule[Text]):
    async def check(self, message: Message, ctx: dict) -> bool:
        return self.inner_rule.check_text(message.text, [
            ctx[I18N_KWARG_NAME].get(text) for text in self.inner_rule.texts
        ])
