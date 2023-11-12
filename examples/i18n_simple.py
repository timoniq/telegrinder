import logging

from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot.rules import Text
from telegrinder.tools.i18n import ABCTranslatorMiddleware, SimpleI18n, SimpleTranslator

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)
i18n = SimpleI18n(folder="examples/assets/i18n", domain="messages", default_locale="en")


class I18nMiddleware(ABCTranslatorMiddleware):
    async def get_locale(self, event) -> str:
        return event.from_user.language_code


@bot.on.message(Text("/test"))
@bot.on.message(Text(["hi", "hello"], ignore_case=True))
async def handler(message: Message, _: SimpleTranslator):
    await message.answer(_("Hello! Your locale is {locale}!", locale=_.locale))

    # SimpleTranslator is locale-aware already
    # And you can also easily format strings inside _()
    await message.answer(_("Hello, {name}!", name=message.from_user.first_name))


bot.on.message.middlewares.append(I18nMiddleware(i18n))
bot.run_forever()
