from telegrinder import API, Message, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import Text

setup_logger()
configure_dotenv()

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(Text("/choice"))
async def action(m: Message):
    chosen, m_id = await (
        bot.dispatch.choice(m.chat.id, message="Choose something", max_in_row=1)
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .add_option("pear", "Pear 🔴", "Pear 🟢")
        .wait(m.api)
    )
    await m.edit(text=f"You chose - {chosen}", message_id=m_id)


bot.run_forever()
