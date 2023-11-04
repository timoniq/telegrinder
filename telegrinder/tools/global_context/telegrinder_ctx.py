import typing

import vbml

from .global_context import GlobalContext, ctx_field


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

    vbml_patcher: typing.Final = ctx_field(vbml.Patcher(), const=True)
