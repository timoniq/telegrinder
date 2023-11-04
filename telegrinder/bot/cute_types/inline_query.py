import typing

from telegrinder.api import ABCAPI, API, APIError
from telegrinder.result import Result
from telegrinder.types import InlineQuery, InlineQueryResult, User


class InlineQueryCute(InlineQuery):
    api: ABCAPI

    @property
    def ctx_api(self) -> API:
        return self.api  # type: ignore

    @property
    def from_user(self) -> User:
        return self.from_

    @classmethod
    def from_update(cls, update: InlineQuery, bound_api: ABCAPI) -> typing.Self:
        return cls(**update.to_dict(), api=bound_api)

    async def answer(
        self,
        results: list[InlineQueryResult | dict] | None = None,
        cache_time: int | None = None,
        is_personal: bool | None = None,
        next_offset: str | None = None,
        switch_pm_text: str | None = None,
        switch_pm_parameter: str | None = None,
    ) -> Result[bool, APIError]:
        return await self.ctx_api.answer_inline_query(
            self.id,
            results=results,  # type: ignore
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter,
        )  # NOTE: param results: implement dataclass instead of dict

    def to_dict(self) -> dict[str, typing.Any]:
        return super().to_dict(exclude_fields={"api"})
