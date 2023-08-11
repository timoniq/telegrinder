from telegrinder import Telegrinder, API, Token, Message
from telegrinder.bot.rules import Text
from telegrinder.tools.i18n import (
    SimpleI18n, SimpleTranslator, ABCTranslatorMiddleware
)

api = API(token=Token.from_env())
bot = Telegrinder(api)
i18n = SimpleI18n(folder="examples/assets/i18n", domain="messages", default_locale="en")


class I18nMiddleware(ABCTranslatorMiddleware):
    async def get_locale(self, event) -> str:
        return event.from_user.language_code


@bot.on.message(Text("/test"))
async def handler(message: Message, _: SimpleTranslator):
    await message.answer(_(
        'Hello! Your locale is {locale}!', locale=_.locale
    ))


bot.dispatch.message.middlewares.append(I18nMiddleware(i18n, "_"))
bot.run_forever()
