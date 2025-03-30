import re

from vbml.patcher.abc import ABCPatcher
from vbml.patcher.patcher import Patcher

from telegrinder.tools.global_context.global_context import GlobalContext, ctx_var, runtime_init
from telegrinder.tools.loop_wrapper import LoopWrapper


@runtime_init
class TelegrinderContext(GlobalContext):
    """The type-hinted telegrinder context called `telegrinder`.

    Example:
    ```
    from telegrinder.tools.global_context import GlobalContext, TelegrinderContext

    telegrinder_ctx = TelegrinderContext(...)  # with type-hints
    assert telegrinder_ctx == GlobalContext("telegrinder")  # ok
    ```

    """

    __ctx_name__ = "telegrinder"

    vbml_pattern_flags: re.RegexFlag | None = ctx_var(default=None, init=False)
    vbml_patcher: ABCPatcher = ctx_var(default_factory=Patcher, init=False)
    loop_wrapper: LoopWrapper = ctx_var(default_factory=LoopWrapper, init=False)


__all__ = ("TelegrinderContext",)
