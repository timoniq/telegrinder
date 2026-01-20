from __future__ import annotations

import re
import typing

from kungfu.library.monad.option import NOTHING, Option
from nodnod.scope import Scope
from vbml.patcher.abc import ABCPatcher
from vbml.patcher.patcher import Patcher

from telegrinder.modules import logger
from telegrinder.tools.global_context.global_context import GlobalContext, ctx_var, runtime_init
from telegrinder.tools.loop_wrapper import LoopWrapper

if typing.TYPE_CHECKING:
    from telegrinder.bot.dispatch.middleware.box import MiddlewareBox


@runtime_init
class TelegrinderContext(GlobalContext, thread_safe=True):
    """The thread-safe type-hinted telegrinder context.

    Example:
    ```
    from telegrinder.tools.global_context import GlobalContext, TelegrinderContext

    telegrinder_ctx = TelegrinderContext(...)  # with type-hints
    assert telegrinder_ctx == GlobalContext("telegrinder")  # ok
    ```

    """

    __ctx_name__ = "telegrinder"

    node_global_scope: Scope = ctx_var(default_factory=lambda: Scope(detail="global"), init=False)
    middleware_box: Option[MiddlewareBox] = ctx_var(default=NOTHING, init=False)
    vbml_pattern_flags: re.RegexFlag | None = ctx_var(default=None, init=False)
    vbml_patcher: ABCPatcher = ctx_var(default_factory=Patcher, init=False)
    loop_wrapper: LoopWrapper = ctx_var(default_factory=LoopWrapper, init=False)

    async def close_global_scope(self) -> None:
        await self.node_global_scope.close()
        logger.debug("Node global scope closed")


__all__ = ("TelegrinderContext",)
