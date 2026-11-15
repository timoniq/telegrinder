import dataclasses
import typing

from telegrinder.tools.backoff.abc import ABCBackoff

DEFAULT_CAP: typing.Final = 2.048
DEFAULT_BASE: typing.Final = 0.128


@dataclasses.dataclass(kw_only=True, frozen=True)
class Backoff(ABCBackoff):
    seconds: float

    def compute(self, failures: int) -> float:
        return self.seconds


@dataclasses.dataclass(kw_only=True, frozen=True)
class BackoffConfig:
    cap: float = DEFAULT_CAP
    """Maximum backoff between each retry (`seconds`)."""

    base: float = DEFAULT_BASE
    """Minimum backoff between each retry (`seconds`)."""


__all__ = ("Backoff", "BackoffConfig")
