from telegrinder import API, Choice, Message, Telegrinder, Token, WaiterMachine
from telegrinder.bot.dispatch.waiter_machine.hasher.callback import CALLBACK_QUERY_FOR_MESSAGE
from telegrinder.rules import Text

api = API(token=Token.from_env())
bot = Telegrinder(api)
wm = WaiterMachine()


@bot.on.message(Text("/choice"))
async def action(m: Message):
    chosen, m_id = await (
        Choice(wm, m.chat.id, "Choose something", max_in_row=1)
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .add_option("pear", "Pear 🔴", "Pear 🟢")
        .wait(CALLBACK_QUERY_FOR_MESSAGE, bot.on.callback_query, m.api)
    )
    await m.edit(text=f"You chose - {chosen}", message_id=m_id)


bot.run_forever()
