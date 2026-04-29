from telegrinder import API, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.node import BaseTranslator, I18NConfig, KeySeparator, UserSource
from telegrinder.rules import Text

configure_dotenv()
setup_logger()


bot = Telegrinder(API(Token.from_env()))


BaseTranslator.configure(I18NConfig(domain="messages", folder="examples/assets/i18n"))
KeySeparator.set(" ")


@bot.on.message(Text("hi"))
async def hi(_: BaseTranslator) -> str:
    return _.hi()


@bot.on.message(Text("hello"))
async def hello(_: BaseTranslator, user: UserSource) -> str:
    return _("Hello, {name}!", name=user.full_name)


@bot.on.message(Text("how are you?"))
async def how_are_you(_: BaseTranslator) -> str:
    return _.im.fine()


bot.run_forever()
