from telegrinder import API, Telegrinder, Token, configure_dotenv, setup_logger
from telegrinder.rules import PaymentInvoiceCurrency
from telegrinder.types.enums import Currency

configure_dotenv()
setup_logger()


bot = Telegrinder(API(Token.from_env()))


@bot.on.pre_checkout_query(PaymentInvoiceCurrency(Currency.XTR))
async def handle_invoice_telegram_stars() -> bool:
    return True  # answer success!


bot.run_forever()
