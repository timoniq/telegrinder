import re

import vbml

from telegrinder.tools.global_context import GlobalContext, ctx_var


class TelegrinderContext(GlobalContext):
    """Basic type-hinted telegrinder context with context name `"telegrinder"`.

    You can use this class or GlobalContext:
    ```
    from telegrinder.tools.global_context import GlobalContext, TelegrinderContext

    ctx1 = TelegrinderContext()
    ctx2 = GlobalContext("telegrinder")  # same, but without the type-hints
    assert ctx1 == ctx2  # ok
    ```
    """

    __ctx_name__ = "telegrinder"

    vbml_pattern_flags: re.RegexFlag | None = None
    vbml_patcher: vbml.Patcher = ctx_var(default=vbml.Patcher(), frozen=True)


__all__ = ("TelegrinderContext",)
