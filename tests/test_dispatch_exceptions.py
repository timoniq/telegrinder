import asyncio

import pytest

from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.dispatch import Dispatch
from telegrinder.bot.dispatch.router.base import Router
from telegrinder.bot.rules.abc import Never


def exception_leaves(exception: BaseException) -> list[BaseException]:
    if isinstance(exception, BaseExceptionGroup):
        return [leaf for child in exception.exceptions for leaf in exception_leaves(child)]
    return [exception]


@pytest.mark.asyncio()
async def test_process_exception_without_handlers(api_instance, message_update, message_context):
    dispatch = Dispatch()
    assert (
        await dispatch._process_exception(ValueError("original"), api_instance, message_update, message_context)
        is False
    )


@pytest.mark.asyncio()
async def test_process_exception_global_handler(api_instance, message_update, message_context):
    dispatch = Dispatch()
    original = ValueError("original")
    seen = []

    @dispatch.error_handler()
    async def handle(ctx: Context):
        seen.append(ctx.exception_update.unwrap())

    assert await dispatch._process_exception(original, api_instance, message_update, message_context) is True
    assert seen == [original]
    assert not message_context.exception_update


@pytest.mark.asyncio()
async def test_process_exception_rejected_global_filter(api_instance, message_update, message_context):
    dispatch = Dispatch()
    original = ValueError("original")
    dispatch.error_handler.filter = Never()

    @dispatch.error_handler()
    async def handle():
        pytest.fail("A rejected error view must not run")

    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exception(original, api_instance, message_update, message_context)
    assert exception_leaves(caught.value) == [original]


@pytest.mark.asyncio()
async def test_process_exception_nested_group(api_instance, message_update, message_context):
    dispatch = Dispatch()
    first, second = ValueError("first"), TypeError("second")
    seen = []

    @dispatch.error_handler()
    async def handle(ctx: Context):
        seen.append(ctx.exception_update.unwrap())

    group = ExceptionGroup("outer", [first, ExceptionGroup("inner", [second])])
    assert await dispatch._process_exception(group, api_instance, message_update, message_context) is True
    assert seen == [first, second]


@pytest.mark.asyncio()
async def test_exceptions_update_only_reports_unhandled(api_instance, message_update, message_context):
    dispatch = Dispatch()
    handled_router, rejected_router = Router(), Router()
    handled, rejected = ValueError("handled"), TypeError("rejected")
    seen = []

    @handled_router.event_error()
    async def handle(ctx: Context):
        seen.append(ctx.exception_update.unwrap())

    rejected_router.event_error.filter = Never()

    @rejected_router.event_error()
    async def reject():
        pytest.fail("A rejected error view must not run")

    message_context.exceptions_update.update({handled_router: handled, rejected_router: rejected})
    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exceptions_update(api_instance, message_update, message_context)
    assert exception_leaves(caught.value) == [rejected]
    assert seen == [handled]


@pytest.mark.asyncio()
async def test_process_exception_router_then_global(api_instance, message_update, message_context):
    dispatch = Dispatch()
    original = ValueError("original")
    seen = []

    @dispatch.event_error(Never())
    async def reject():
        pytest.fail("A rejected handler must not run")

    @dispatch.error_handler()
    async def handle(ctx: Context):
        seen.append(ctx.exception_update.unwrap())

    message_context.exceptions_update[dispatch.main_router] = original
    assert await dispatch._process_exception(original, api_instance, message_update, message_context) is True
    assert seen == [original]


@pytest.mark.parametrize("global_handler", [False, True])
@pytest.mark.asyncio()
async def test_process_exception_preserves_unregistered_errors(
    api_instance, message_update, message_context, global_handler
):
    dispatch = Dispatch()
    handled, other = ValueError("handled"), TypeError("other")
    seen = []

    @dispatch.event_error()
    async def handle_router():
        pass

    if global_handler:

        @dispatch.error_handler()
        async def handle_global(ctx: Context):
            seen.append(ctx.exception_update.unwrap())

    message_context.exceptions_update[dispatch.main_router] = handled
    group = ExceptionGroup("routing", [handled, other])
    if global_handler:
        assert await dispatch._process_exception(group, api_instance, message_update, message_context) is True
        assert seen == [other]
    else:
        with pytest.raises(BaseExceptionGroup) as caught:
            await dispatch._process_exception(group, api_instance, message_update, message_context)
        assert exception_leaves(caught.value) == [other]


@pytest.mark.parametrize("router_handler", [False, True])
@pytest.mark.asyncio()
async def test_failed_error_handler_preserves_original_and_failure(
    api_instance, message_update, message_context, router_handler
):
    dispatch = Dispatch()
    original, failure = ValueError("original"), RuntimeError("handler failed")
    view = dispatch.event_error if router_handler else dispatch.error_handler
    if router_handler:
        message_context.exceptions_update[dispatch.main_router] = original

    @view()
    async def handle():
        raise failure

    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exception(original, api_instance, message_update, message_context)
    assert sorted(exception_leaves(caught.value), key=id) == sorted([original, failure], key=id)


@pytest.mark.parametrize("router_handler", [False, True])
@pytest.mark.asyncio()
async def test_cancelled_error_handler_is_unhandled(api_instance, message_update, message_context, router_handler):
    dispatch = Dispatch()
    original = ValueError("original")
    view = dispatch.event_error if router_handler else dispatch.error_handler
    if router_handler:
        message_context.exceptions_update[dispatch.main_router] = original

    @view()
    async def handle():
        raise asyncio.CancelledError

    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exception(original, api_instance, message_update, message_context)
    assert exception_leaves(caught.value) == [original]


@pytest.mark.asyncio()
async def test_process_exception_router_handler_has_priority(api_instance, message_update, message_context):
    dispatch = Dispatch()
    original = ValueError("original")
    seen = []

    @dispatch.event_error()
    async def handle_router(ctx: Context):
        seen.append(ctx.exception_update.unwrap())

    @dispatch.error_handler()
    async def handle_global():
        pytest.fail("An already handled error must not reach the global handler")

    message_context.exceptions_update[dispatch.main_router] = original
    group = ExceptionGroup("routing", [original])
    assert await dispatch._process_exception(group, api_instance, message_update, message_context) is True
    assert seen == [original]


@pytest.mark.asyncio()
async def test_process_exception_no_matching_error_handler(api_instance, message_update, message_context):
    dispatch = Dispatch()
    original = ValueError("original")

    @dispatch.error_handler(Never())
    async def reject():
        pytest.fail("A rejected handler must not run")

    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exception(original, api_instance, message_update, message_context)
    assert exception_leaves(caught.value) == [original]


@pytest.mark.asyncio()
async def test_process_exception_does_not_duplicate_reraised_router_group(
    api_instance, message_update, message_context
):
    dispatch = Dispatch()
    original = ValueError("original")
    group = ExceptionGroup("outer", [ExceptionGroup("inner", [original])])

    @dispatch.event_error(Never())
    async def reject():
        pytest.fail("A rejected handler must not run")

    message_context.exceptions_update[dispatch.main_router] = group
    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exception(group, api_instance, message_update, message_context)
    assert exception_leaves(caught.value) == [original]


@pytest.mark.asyncio()
async def test_handle_exceptions_accepts_iterator(api_instance, message_update, message_context):
    dispatch = Dispatch()
    errors = [ValueError("first"), TypeError("second")]
    seen = []

    @dispatch.error_handler()
    async def handle(ctx: Context):
        seen.append(ctx.exception_update.unwrap())

    await dispatch._handle_exceptions(api_instance, message_update, message_context, iter(errors))
    assert seen == errors


@pytest.mark.parametrize("exception_type", [KeyboardInterrupt, SystemExit])
@pytest.mark.parametrize("nested", [False, True])
@pytest.mark.asyncio()
async def test_process_exception_reraises_system_exceptions(
    api_instance, message_update, message_context, exception_type, nested
):
    dispatch = Dispatch()
    original = exception_type()

    @dispatch.error_handler()
    async def handle():
        pytest.fail("System exceptions must not reach the error handler")

    exception = BaseExceptionGroup("system", [original]) if nested else original
    with pytest.raises(exception_type) as caught:
        await dispatch._process_exception(exception, api_instance, message_update, message_context)
    assert caught.value is original


@pytest.mark.asyncio()
async def test_failed_router_handler_preserves_cancelled_sibling(api_instance, message_update, message_context):
    dispatch = Dispatch()
    failing_router, waiting_router = Router(), Router()
    first, second = ValueError("first"), TypeError("second")
    failure = RuntimeError("handler failed")
    started, cancelled = asyncio.Event(), asyncio.Event()

    @failing_router.event_error()
    async def fail():
        await started.wait()
        raise failure

    @waiting_router.event_error()
    async def wait():
        started.set()
        try:
            await asyncio.Future()
        finally:
            cancelled.set()

    message_context.exceptions_update.update({failing_router: first, waiting_router: second})
    with pytest.raises(BaseExceptionGroup) as caught:
        await dispatch._process_exceptions_update(api_instance, message_update, message_context)
    assert sorted(exception_leaves(caught.value), key=id) == sorted([first, second, failure], key=id)
    assert cancelled.is_set()
