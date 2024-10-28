import abc
import typing

from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.rules.abc import ABCRule, CheckResult
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.types.enums import Currency, UpdateType

PreCheckoutQuery: typing.TypeAlias = PreCheckoutQueryCute


class PaymentInvoiceRule(ABCRule[PreCheckoutQuery], abc.ABC):
    adapter: EventAdapter[PreCheckoutQuery] = EventAdapter(
        UpdateType.PRE_CHECKOUT_QUERY,
        PreCheckoutQuery,
    )

    @abc.abstractmethod
    def check(self, *args: typing.Any, **kwargs: typing.Any) -> CheckResult: ...


class PaymentInvoiceCurrency(PaymentInvoiceRule):
    def __init__(self, currency: str | Currency, /) -> None:
        self.currency = currency

    def check(self, query: PreCheckoutQuery) -> bool:
        return self.currency == query.currency


__all__ = ("PaymentInvoiceCurrency", "PaymentInvoiceRule")
