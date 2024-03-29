from telegrinder import API, Checkbox, Message, Telegrinder, Token, WaiterMachine
from telegrinder.rules import Text
from telegrinder.modules import logger

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

logger.set_level("INFO")


@bot.on.message(Text("/checkbox"))
async def action(m: Message):
    picked, m_id = await (
        Checkbox(wm, m.chat.id, "Check your checkbox", max_in_row=2)
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .add_option("pear", "Pear", "Pear 🍐")
        .wait(m.ctx_api, bot.dispatch.callback_query)
    )
    await m.ctx_api.edit_message_text(
        chat_id=m.chat.id,
        message_id=m_id,
        text="You picked: {}".format(", ".join([c for c in picked if picked[c]])),
    )


bot.run_forever()
