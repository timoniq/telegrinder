from telegrinder import API, Message, Telegrinder, Token
from telegrinder.modules import configure_dotenv, setup_logger
from telegrinder.rules import Text

configure_dotenv()
setup_logger()

api = API(token=Token.from_env())
bot = Telegrinder(api)


@bot.on.message(Text("/checkbox"))
async def action(m: Message) -> None:
    picked, m_id = await (
        bot.dispatch.checkbox(m.chat_id, message="Check your checkbox", cancel_text="Cancel", max_in_row=2)
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .add_option("pear", "Pear", "Pear 🍐")
        .wait(m.api)
    )
    await m.edit(
        text="You picked: {}".format(", ".join(c for c in picked if picked[c])),
        chat_id=m.chat.id,
        message_id=m_id,
    )


bot.run_forever()
