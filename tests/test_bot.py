import asyncio
import io
import logging
from collections import deque

import pytest

from telegrinder.bot.dispatch.dispatch import Dispatch
from telegrinder.modules import (
    _configure_logging,
    _configure_loguru,
    log_scope,
    logger,
    wrap_logging_logger,
    wrap_loguru_logger,
    wrap_structlog_logger,
)


@pytest.mark.asyncio()
async def test_log_scope_is_nested():
    sink = io.StringIO()
    _configure_logging("DEBUG", None, False, sink)

    with log_scope("outer"), log_scope("inner"):
        await logger.ainfo("hello")

    assert "[outer > inner] hello" in sink.getvalue()


@pytest.mark.asyncio()
async def test_log_buffer_preserves_original_log_frame():
    sink = io.StringIO()
    _configure_logging("DEBUG", None, False, sink)

    async def demo() -> None:
        from telegrinder.modules import log_buffer

        with log_buffer("Update:1"), log_scope("scope"):
            await logger.ainfo("hello")

    await demo()

    output = sink.getvalue()
    assert "__main__" not in output
    assert "modules:<lambda>" not in output
    assert "demo:" in output


@pytest.mark.asyncio()
async def test_dispatch_feed_flushes_buffered_logs_in_one_block(api_instance, message_update, monkeypatch):
    sink = io.StringIO()
    _configure_logging("DEBUG", None, False, sink)

    dispatch = Dispatch()
    dispatch._routers = deque([dispatch.main_router])
    first_log_written = asyncio.Event()
    second_log_written = asyncio.Event()

    async def fake_route_update(*_args):
        async def first_router() -> None:
            with log_scope("router-1"):
                await logger.ainfo("first")
                assert sink.getvalue() == ""
                first_log_written.set()
                await second_log_written.wait()
                await logger.ainfo("third")
                assert sink.getvalue() == ""

        async def second_router() -> None:
            await first_log_written.wait()
            with log_scope("router-2"):
                await logger.ainfo("second")
                assert sink.getvalue() == ""
                second_log_written.set()

        async with dispatch.loop_wrapper.create_task_group() as task_group:
            task_group.create_task(first_router())
            task_group.create_task(second_router())

    monkeypatch.setattr(dispatch, "_route_update", fake_route_update)

    await dispatch.feed(api_instance, message_update)

    output = sink.getvalue()
    assert output.index("first") < output.index("third") < output.index("second")
    assert "[Update:12345 > router-1] first" in output
    assert "[Update:12345 > router-1] third" in output
    assert "[Update:12345 > router-2] second" in output


@pytest.mark.asyncio()
async def test_dispatch_feed_flushes_buffered_loguru_logs(api_instance, message_update, monkeypatch):
    pytest.importorskip("loguru")

    sink = io.StringIO()
    _configure_loguru("DEBUG", None, False, sink)

    dispatch = Dispatch()
    dispatch._routers = deque([dispatch.main_router])
    first_log_written = asyncio.Event()
    second_log_written = asyncio.Event()

    async def fake_route_update(*_args):
        async def first_router() -> None:
            with log_scope("router-1"):
                await logger.ainfo("first")
                assert sink.getvalue() == ""
                first_log_written.set()
                await second_log_written.wait()
                await logger.ainfo("third")
                assert sink.getvalue() == ""

        async def second_router() -> None:
            await first_log_written.wait()
            with log_scope("router-2"):
                await logger.ainfo("second")
                assert sink.getvalue() == ""
                second_log_written.set()

        async with dispatch.loop_wrapper.create_task_group() as task_group:
            task_group.create_task(first_router())
            task_group.create_task(second_router())

    monkeypatch.setattr(dispatch, "_route_update", fake_route_update)

    await dispatch.feed(api_instance, message_update)

    output = sink.getvalue()
    assert output.index("first") < output.index("third") < output.index("second")
    assert "[Update:12345 > router-1] first" in output
    assert "[Update:12345 > router-1] third" in output
    assert "[Update:12345 > router-2] second" in output


@pytest.mark.asyncio()
async def test_set_logger_with_wrapped_logging_logger_preserves_buffered_dispatch_logs(
    api_instance,
    message_update,
    monkeypatch,
):
    sink = io.StringIO()
    custom_logger = logging.getLogger("telegrinder.custom")
    custom_logger.handlers[:] = []
    custom_logger.propagate = False
    custom_logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sink)
    handler.setFormatter(logging.Formatter("{message}", style="{"))
    custom_logger.addHandler(handler)

    logger.set_logger(wrap_logging_logger(custom_logger), "logging")  # type: ignore

    dispatch = Dispatch()
    dispatch._routers = deque([dispatch.main_router])
    first_log_written = asyncio.Event()
    second_log_written = asyncio.Event()

    async def fake_route_update(*_args):
        async def first_router() -> None:
            with log_scope("router-1"):
                await logger.ainfo("first")
                assert sink.getvalue() == ""
                first_log_written.set()
                await second_log_written.wait()
                await logger.ainfo("third")
                assert sink.getvalue() == ""

        async def second_router() -> None:
            await first_log_written.wait()
            with log_scope("router-2"):
                await logger.ainfo("second")
                assert sink.getvalue() == ""
                second_log_written.set()

        async with dispatch.loop_wrapper.create_task_group() as task_group:
            task_group.create_task(first_router())
            task_group.create_task(second_router())

    monkeypatch.setattr(dispatch, "_route_update", fake_route_update)

    await dispatch.feed(api_instance, message_update)

    output = sink.getvalue()
    assert output.index("first") < output.index("third") < output.index("second")
    assert "[Update:12345 > router-1] first" in output
    assert "[Update:12345 > router-2] second" in output


@pytest.mark.asyncio()
async def test_set_logger_without_wrapper_keeps_immediate_logging(api_instance, message_update, monkeypatch):
    sink = io.StringIO()
    custom_logger = logging.getLogger("telegrinder.custom.unwrapped")
    custom_logger.handlers[:] = []
    custom_logger.propagate = False
    custom_logger.setLevel(logging.DEBUG)

    handler = logging.StreamHandler(sink)
    handler.setFormatter(logging.Formatter("{message}", style="{"))
    custom_logger.addHandler(handler)

    logger.set_logger(custom_logger, "logging")  # type: ignore

    dispatch = Dispatch()
    dispatch._routers = deque([dispatch.main_router])
    first_log_written = asyncio.Event()

    async def fake_route_update(*_args):
        async def first_router() -> None:
            with log_scope("router-1"):
                await logger.ainfo("first")
                assert sink.getvalue() != ""
                first_log_written.set()

        async def second_router() -> None:
            await first_log_written.wait()
            with log_scope("router-2"):
                await logger.ainfo("second")

        async with dispatch.loop_wrapper.create_task_group() as task_group:
            task_group.create_task(first_router())
            task_group.create_task(second_router())

    monkeypatch.setattr(dispatch, "_route_update", fake_route_update)

    await dispatch.feed(api_instance, message_update)

    output = sink.getvalue()
    assert "first" in output
    assert "second" in output


def test_wrap_structlog_logger_buffers_stream_handlers():
    custom_logger = logging.getLogger("telegrinder.structlog.custom")
    custom_logger.handlers[:] = []
    custom_logger.addHandler(logging.StreamHandler(io.StringIO()))

    class StructLoggerStub:
        def __init__(self, raw_logger: logging.Logger) -> None:
            self._logger = raw_logger

    wrapped = wrap_structlog_logger(StructLoggerStub(custom_logger))
    assert wrapped._logger.handlers
    assert wrapped._logger.handlers[0].__class__.__name__ == "BufferedStreamHandler"


def test_wrap_logging_logger_buffers_stream_handlers():
    custom_logger = logging.getLogger("telegrinder.logging.custom")
    custom_logger.handlers[:] = []
    custom_logger.addHandler(logging.StreamHandler(io.StringIO()))

    wrapped = wrap_logging_logger(custom_logger)
    assert wrapped.handlers
    assert wrapped.handlers[0].__class__.__name__ == "BufferedStreamHandler"


def test_wrap_loguru_logger_rejects_invalid_logger():
    with pytest.raises(TypeError):
        wrap_loguru_logger(object())
