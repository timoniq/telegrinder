from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.types.enums import Currency


class PaymentInvoiceCurrency(ABCRule):
    def __init__(self, currency: Currency, /) -> None:
        self.currency = currency

    def check(self, query: PreCheckoutQueryCute) -> bool:
        return self.currency == query.currency


__all__ = ("PaymentInvoiceCurrency",)
