from telegrinder import API, Checkbox, Message, Telegrinder, Token, WaiterMachine
from telegrinder.bot.dispatch.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE
from telegrinder.modules import setup_logger
from telegrinder.rules import Text

setup_logger()

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()


@bot.on.message(Text("/checkbox"))
async def action(m: Message) -> None:
    picked, m_id = await (
        Checkbox(wm, m.chat.id, "Check your checkbox", cancel_text="Cancel", max_in_row=2)
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .add_option("pear", "Pear", "Pear 🍐")
        .wait(CALLBACK_QUERY_FOR_MESSAGE, bot.on.callback_query, m.ctx_api)
    )
    await m.edit(
        text="You picked: {}".format(", ".join(c for c in picked if picked[c])),
        chat_id=m.chat.id,
        message_id=m_id,
    )


bot.run_forever()
