from __future__ import annotations

import dataclasses
import typing

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.router.abc import ABCRouter
from telegrinder.bot.dispatch.view.box import ViewBox
from telegrinder.modules import logger
from telegrinder.tools.magic.inspect import get_frame_module_name
from telegrinder.types.objects import Update

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.view.base import View


@dataclasses.dataclass(kw_only=True)
class Router(ABCRouter, ViewBox):
    def __post_init__(self) -> None:
        self.name = ":".join((get_frame_module_name(), self.__class__.__name__, hex(id(self))))

    def __repr__(self) -> str:
        return f"<{self.name}>"

    def __hash__(self) -> int:
        return hash(self.name)

    def __bool__(self) -> bool:
        return any(self.views.values()) or bool(self.raw) or bool(self.error)

    async def route_view(self, view: View, api: API, update: Update, context: Context) -> bool:
        # Check if the view is applicable to the update
        if await view.check(api, update, context):
            await logger.adebug(
                "Processing update (id={}, type={!r}) with view `{!r}` from router `{!r}`",
                update.update_id,
                update.update_type,
                view,
                self,
            )
            result = await view.process(api, update, context)
            await logger.ainfo(
                "Update(id={}, type={!r}) processed with view `{!r}` from router `{!r}`. {}",
                update.update_id,
                update.update_type,
                view,
                self,
                result.error if not result else result.value,
            )
            return bool(result)

        # View is not applicable to the update
        return False

    async def route(self, api: API, update: Update, context: Context) -> bool:
        try:
            # Filtering non-empty views
            for view in filter(None, self.views.values()):
                # Route the non-empty view
                if await self.route_view(view, api, update, context):
                    return True

            # No views are applicable to the update
            return False
        except Exception as exception:
            context.exceptions_update[self] = exception
            raise


__all__ = ("Router",)
