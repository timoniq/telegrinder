from telegrinder import API, Message, Telegrinder, Token
from telegrinder.bot.rules import Text
from telegrinder.modules import logger
from telegrinder.tools.i18n import ABCTranslatorMiddleware, SimpleI18n, SimpleTranslator

api = API(token=Token.from_env())
bot = Telegrinder(api)
i18n = SimpleI18n(folder="examples/assets/i18n", domain="messages", default_locale="en")

logger.set_level("INFO")


@bot.on.message.register_middleware()
class I18nMiddleware(ABCTranslatorMiddleware[Message]):
    async def get_locale(self, event: Message) -> str:
        return event.from_user.language_code.unwrap()


@bot.on.message(Text(["hi", "hello"], ignore_case=True) | Text("/test"))
async def handler(message: Message, _: SimpleTranslator):
    await message.answer(_("Hello! Your locale is {locale}!", locale=_.locale))

    # SimpleTranslator is locale-aware already
    # And you can also easily format strings inside _()
    await message.answer(_("Hello, {name}!", name=message.from_user.first_name))


bot.run_forever()
