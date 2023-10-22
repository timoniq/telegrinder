import logging

from telegrinder import API, Message, SingleChoice, Telegrinder, Token, WaiterMachine
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
logging.basicConfig(level=logging.DEBUG)

wm = WaiterMachine()


@bot.on.message(Text("/choice"))
async def action(m: Message):
    chosen, m_id = await (
        SingleChoice(wm, m.chat.id, "Choose something", max_in_row=2)
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .add_option("pear", "Pear 🔴", "Pear 🟢")
        .wait(m.ctx_api, bot.dispatch)
    )
    await m.ctx_api.edit_message_text(
        m.chat.id,
        m_id,
        text=f"You chose {chosen}",
    )


bot.run_forever()
