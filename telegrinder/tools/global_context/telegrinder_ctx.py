import typing

import vbml

from telegrinder.tools.global_context import GlobalContext, ctx_var


class TelegrinderCtx(GlobalContext):
    """Basic typed telegrinder context named `"telegrinder"`.
    You can use this class or GlobalContext.
    ```
    from telegrinder.tools.global_context import GlobalContext, TelegrinderCtx

    ctx1 = TelegrinderCtx()
    ctx2 = GlobalContext("telegrinder")  # same, but without the typehints
    assert ctx1 == ctx2
    ```"""

    __ctx_name__ = "telegrinder"

    vbml_patcher: typing.ClassVar = ctx_var(vbml.Patcher(), const=True)
