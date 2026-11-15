import dataclasses
import random

from telegrinder.tools.backoff.abc import ABCBackoff
from telegrinder.tools.backoff.base import BackoffConfig


@dataclasses.dataclass(kw_only=True, frozen=True)
class ExponentialBackoff(ABCBackoff, BackoffConfig):
    jitter: bool = False
    """Exponential backoff with jitter if enabled."""

    @staticmethod
    def compute_exponential(config: BackoffConfig, failures: int, /) -> float:
        return min(config.cap, config.base * 2**failures)

    @staticmethod
    def compute_exponential_with_jitter(config: BackoffConfig, failures: int, /) -> float:
        return min(config.cap, random.random() * config.base * 2**failures)

    def compute(self, failures: int) -> float:
        return (
            self.compute_exponential_with_jitter(self, failures)
            if self.jitter is True
            else self.compute_exponential(self, failures)
        )


__all__ = ("ExponentialBackoff",)
