from telegrinder import API, Choice, Message, Telegrinder, Token, WaiterMachine
from telegrinder.modules import logger
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine(bot.dispatch)

logger.set_level("INFO")


@bot.on.message(Text("/choice"))
async def action(m: Message):
    chosen, m_id = await (
        Choice(wm, m.chat.id, "Choose something", max_in_row=1)
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .add_option("pear", "Pear 🔴", "Pear 🟢")
        .wait(m.ctx_api, bot.dispatch.callback_query)
    )
    await m.edit(text=f"You chose - {chosen}", message_id=m_id)


bot.run_forever()
