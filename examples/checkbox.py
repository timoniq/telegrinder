from telegrinder import Telegrinder, API, Token, Message, Checkbox, WaiterMachine
from telegrinder.rules import Text
import logging

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()

logging.basicConfig(level=logging.DEBUG)


@bot.on.message(Text("/checkbox"))
async def action(m: Message):
    picked, m_id = await (
        Checkbox(wm, m.chat.id, "Check your checkbox", max_in_row=2)
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .add_option("pear", "Pear", "Pear 🍐")
        .wait(m.ctx_api, bot.dispatch)
    )
    await m.ctx_api.edit_message_text(
        m.chat.id,
        m_id,
        text="You picked: {}".format(", ".join([c for c in picked if picked[c]])),
    )


bot.run_forever()
