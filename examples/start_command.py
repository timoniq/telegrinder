from telegrinder import API, Message, Telegrinder, Token
from telegrinder.rules import StartCommand

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(StartCommand(lambda x: (int(x) if x.isdigit() else None)))
async def start_handler(message: Message, param: int | None) -> None:
    if param is None:
        await message.answer("You have no integer start query((")
        return
    await message.answer(
        "Ahah you integer start query is so funny, its {0} and {0}-42={1}".format(param, param - 42)
    )


@bot.on.message(StartCommand(param_required=True, alias="name"))
async def start_with_name(message: Message, name: str):
    await message.reply(f"Hello, {name!r}!")


bot.run_forever()
