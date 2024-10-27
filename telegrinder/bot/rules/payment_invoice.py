import abc
import typing

from telegrinder.bot.cute_types.pre_checkout_query import PreCheckoutQueryCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules.abc import ABCRule, CheckResult
from telegrinder.bot.rules.adapter import EventAdapter
from telegrinder.bot.rules.markup import Markup, PatternLike, check_string
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


class PaymentInvoicePayloadEq(PaymentInvoiceRule):
    def __init__(self, payload: str, /) -> None:
        self.payload = payload

    def check(self, query: PreCheckoutQuery) -> bool:
        return self.payload == query.invoice_payload


class PaymentInvoicePayloadMarkup(PaymentInvoiceRule):
    def __init__(self, patterns: PatternLike | list[PatternLike], /) -> None:
        self.patterns = Markup(patterns).patterns

    def check(self, query: PreCheckoutQuery, ctx: Context) -> bool:
        return check_string(self.patterns, query.invoice_payload, ctx)


__all__ = (
    "PaymentInvoiceCurrency",
    "PaymentInvoicePayloadEq",
    "PaymentInvoicePayloadMarkup",
    "PaymentInvoiceRule",
)
