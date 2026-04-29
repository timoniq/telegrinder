from telegrinder import API, Message, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import StartCommand

configure_dotenv()
setup_logger()


api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(StartCommand(lambda x: int(x) if x.isdigit() else None))
async def start_handler(message: Message, param: int | None) -> None:
    if param is None:
        await message.answer("You have no integer start query((")
        return
    await message.answer("Ahah you integer start query is so funny, its {0} and {0}-42={1}".format(param, param - 42))


bot.run_forever()
