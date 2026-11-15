import dataclasses
import random
from abc import ABC, abstractmethod

from telegrinder.tools.backoff.abc import ABCBackoff
from telegrinder.tools.backoff.base import BackoffConfig
from telegrinder.tools.backoff.exponential import ExponentialBackoff


@dataclasses.dataclass(kw_only=True, frozen=True)
class JitterBackoff(BackoffConfig, ABCBackoff, ABC):
    @abstractmethod
    def compute(self, failures: int) -> float:
        pass


class FullJitterBackoff(JitterBackoff):
    def compute(self, failures: int) -> float:
        return random.uniform(0, ExponentialBackoff.compute_exponential(self, failures))


class EqualJitterBackoff(JitterBackoff):
    def compute(self, failures: int) -> float:
        backoff = ExponentialBackoff.compute_exponential(self, failures) / 2
        return backoff + random.uniform(0, backoff)


__all__ = ("EqualJitterBackoff", "FullJitterBackoff")
