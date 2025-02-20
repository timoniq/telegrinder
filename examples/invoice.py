from telegrinder import API, Telegrinder, Token
from telegrinder.rules import PaymentInvoiceCurrency
from telegrinder.types.enums import Currency

bot = Telegrinder(API(Token.from_env()))

@bot.on.pre_checkout_query(PaymentInvoiceCurrency(Currency.XTR))
async def handle_invoice_telegram_stars() -> bool:
    return True  # answer success!


bot.run_forever()
