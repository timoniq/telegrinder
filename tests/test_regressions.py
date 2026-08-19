"""Regression tests for behavioural bug fixes across the framework.

Each test reproduces a concrete defect: it is written to fail against the buggy behaviour and to
pass once the fix is in place. Where a fix is a pure source-level change (e.g. the syntax of an
exception handler) the test asserts on the source; everywhere else it asserts on behaviour.
"""

import asyncio
import base64
import datetime
import pathlib
import typing
from collections import deque

import msgspec
import pytest
from kungfu.library.monad.option import Nothing, Some
from kungfu.library.monad.result import Error, Ok

from telegrinder.api.api import API, retryer
from telegrinder.api.error import APIError
from telegrinder.api.token import Token
from telegrinder.bot.cute_types.base import compose_method_params
from telegrinder.bot.cute_types.managed_bot_updated import ManagedBotUpdatedCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.cute_types.utils import exclude_bound_parameters
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.dispatch.middleware.box import MiddlewareBox
from telegrinder.bot.dispatch.middleware.filter import FilterMiddleware
from telegrinder.bot.dispatch.middleware.media_group import MediaGroupMiddleware
from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware
from telegrinder.bot.dispatch.return_manager.utils import _get_types
from telegrinder.bot.polling.error_handler import ErrorHandler
from telegrinder.bot.polling.polling import Polling
from telegrinder.bot.rules.abc import ABCRule
from telegrinder.bot.rules.start import StartCommand
from telegrinder.client.wreq_client import WreqClient
from telegrinder.node import NodeError, State, scalar_node
from telegrinder.node.nodes.managed_bot import ManagedBotCreatedBotUsername
from telegrinder.tools.aio import TaskGroup
from telegrinder.tools.formatting.deep_links.parsing import NO_VALUE, parse_query_params
from telegrinder.tools.formatting.html import date_time, escape, link, pre_code, tg_emoji
from telegrinder.tools.global_context import CtxVar, GlobalContext
from telegrinder.tools.keyboard import InlineButton, InlineKeyboard
from telegrinder.tools.lifespan import Lifespan
from telegrinder.tools.limited_dict import LimitedDict
from telegrinder.tools.magic.annotations import get_generic_parameters
from telegrinder.tools.magic.function import resolve_kwonly_arg_names
from telegrinder.tools.serialization import msgpack_ser
from telegrinder.tools.serialization.json_ser import JSONSerializer
from telegrinder.tools.serialization.msgpack_ser import MsgPackSerializer
from telegrinder.tools.singleton.singleton import Singleton, SingletonMeta
from telegrinder.tools.state_mutator.mutation import mutation
from telegrinder.tools.state_storage.memory import MemoryStateStorage
from telegrinder.tools.waiter_machine.hasher import Hasher
from telegrinder.tools.waiter_machine.machine import WaiterMachine
from telegrinder.tools.waiter_machine.short_state import ShortState
from telegrinder.types.enums import UpdateType
from telegrinder.types.objects import ManagedBotUpdated, MessageEntity

from .test_utils import MockedHttpClient, with_mocked_api

REPO_ROOT = pathlib.Path(__file__).resolve().parent.parent


@pytest.fixture(autouse=True)
def _isolate_global_context_storage():
    """Remove any named contexts a test registers, so the suite is re-runnable in one process.

    GlobalContext.__storage__ is a process-global ClassVar; without cleanup a leaked named
    context (e.g. a const var) makes a re-run of these tests fail.
    """
    storage = GlobalContext.__storage__._storage
    before = set(storage)
    yield
    for key in set(storage) - before:
        storage.pop(key, None)


# --------------------------------------------------------------------------- helpers


class _PassRule(ABCRule):
    async def check(self) -> bool:
        return True


class _FailRule(ABCRule):
    async def check(self) -> bool:
        return False


@scalar_node
class _Const42:
    @classmethod
    def __compose__(cls) -> int:
        return 42


@scalar_node
class _Const7:
    @classmethod
    def __compose__(cls) -> int:
        return 7


@scalar_node
class _FailingNode:
    @classmethod
    def __compose__(cls) -> int:
        raise NodeError("boom")


class _Generic[T, *Ts]:  # PEP 695 generic where the TypeVarTuple is NOT the first parameter
    pass


# --------------------------------------------------------------------------- dispatch & middleware


def test_update_cute_decoding_uses_enum_value():
    raw_update = msgspec.json.encode(
        {
            "update_id": 1,
            "message": {
                "message_id": 1,
                "date": 1_713_971_200,
                "chat": {"id": 1, "type": "private", "first_name": "Cute"},
                "text": "hello",
            },
        },
    )

    api = API(Token("123:ABCdef"), http=MockedHttpClient())
    update = UpdateCute.from_raw(raw_update, api)

    assert update.update_type.value == "message"
    assert str(update.update_type) == "message"
    assert isinstance(update.incoming_update, MessageCute)
    assert update.incoming_update.message_id == 1


@pytest.mark.asyncio()
async def test_filter_middleware_passes_through_non_held_updates(message_context: Context):
    mw = FilterMiddleware()
    # Hold a value (999) that the source node never composes to (it composes to 42).
    with mw.hold(_Const42, 999):
        result = await mw.pre(message_context)
    # Buggy behaviour returns False here, dropping the unrelated update (a dispatch-wide DoS).
    assert result is True


@pytest.mark.asyncio()
async def test_filter_middleware_passes_through_uncomposable_updates(message_context: Context):
    mw = FilterMiddleware()
    # The held source node fails to compose (raises NodeError -> compose Error).
    with mw.hold(_FailingNode, 999):
        result = await mw.pre(message_context)
    # The `Error` arm must let the update through (it is not the held one), not drop it.
    assert result is True


@pytest.mark.asyncio()
async def test_filter_middleware_evaluates_every_held_source_node(message_context: Context):
    mw = FilterMiddleware()
    # First hold matches and passes; second hold matches but its rule fails.
    with mw.hold(_Const42, 42, _PassRule()), mw.hold(_Const7, 7, _FailRule()):
        result = await mw.pre(message_context)
    # Buggy behaviour returns True after the first source node and never checks the second.
    assert result is False


def test_media_group_middleware_is_always_active():
    media_group = MediaGroupMiddleware()
    assert not media_group  # empty media_groups -> falsy

    # MiddlewareBox is a Singleton, so MiddlewareBox(...) would return (or create) the process-wide
    # instance other tests share. object.__new__ gives a fresh, isolated box whose fields we set
    # directly, then we drive the real __iter__.
    box = object.__new__(MiddlewareBox)
    box.filter = FilterMiddleware()
    box.media_group = media_group
    box.waiter = WaiterMiddleware(WaiterMachine())
    box.user_middlewares = deque()

    yielded = list(box)
    # The empty filter/waiter stay unyielded (falsy), but gating media_group on its always-empty
    # dict used to drop it too; it must be yielded unconditionally so it can collect groups.
    assert media_group in yielded


@pytest.mark.asyncio()
async def test_pre_middleware_returning_none_does_not_stop_dispatch(message_context: Context):
    from telegrinder.bot.dispatch.middleware.abc import ABCMiddleware, run_pre_middleware

    class ObserveOnly(ABCMiddleware):
        async def pre(self) -> None:  # returns None -> a valid "pass" per the contract
            return None

    # Buggy behaviour did bool(None) -> False, silently stopping all event processing.
    assert await run_pre_middleware(ObserveOnly(), message_context) is True
    # Note: the sibling change (a middleware that fails to COMPOSE stays fail-closed) is not
    # regression-tested: the original used bool(run_middleware()) and bool(None) is already False,
    # so the compose-error path returns False both before and after the fix — nothing to guard.


def test_start_command_tolerates_malformed_deep_link_param():
    rule = StartCommand(decode_deep_link_param=True)
    ctx = Context()
    ctx.set("param", "a")  # invalid base64 padding -> binascii.Error
    # An undecodable, attacker-controlled param must not raise out of check().
    assert rule.check(bot_username="bot", message_entities=Nothing(), ctx=ctx) is False


# --------------------------------------------------------------------------- cute types & API shortcuts


def test_exclude_bound_parameters_flattens_other_and_drops_self():
    params = {"self": object(), "chat_id": 5, "other": {"foo": 1}}
    # Buggy behaviour raised ValueError (iterating a dict yields keys, unpacked as k, v).
    result = exclude_bound_parameters(params)
    assert result == {"chat_id": 5, "foo": 1}


@pytest.mark.asyncio()
async def test_managed_bot_set_access_settings_calls_api():
    api = API(Token("123:ABCdef"), http=MockedHttpClient('{"ok": true, "result": true}'))
    managed = ManagedBotUpdated.from_raw(
        b'{"user": {"id": 1, "is_bot": false, "first_name": "U"}, "bot": {"id": 2, "is_bot": true, "first_name": "B"}}',
    )
    cute = ManagedBotUpdatedCute.from_update(managed, bound_api=api)

    result = await cute.set_access_settings(is_access_restricted=True)
    # The method body was `...`, so it returned None instead of calling the API.
    assert result is not None
    assert result.unwrap() is True


@pytest.mark.asyncio()
async def test_managed_bot_get_access_settings_calls_api():
    api = API(Token("123:ABCdef"), http=MockedHttpClient('{"ok": true, "result": {}}'))
    managed = ManagedBotUpdated.from_raw(
        b'{"user": {"id": 1, "is_bot": false, "first_name": "U"}, "bot": {"id": 2, "is_bot": true, "first_name": "B"}}',
    )
    cute = ManagedBotUpdatedCute.from_update(managed, bound_api=api)

    result = await cute.get_access_settings()
    # get_access_settings was likewise a `...` no-op returning None.
    assert result is not None


def test_compose_method_params_preserves_caller_value(message_update, api_instance):
    from telegrinder.bot.cute_types.message import MessageCute

    update = MessageCute.from_update(message_update.message.unwrap(), bound_api=api_instance)
    params = {"direct_messages_topic_id": 999}
    # Mirror real registration: a bare-string default param + a hook renaming it to the
    # user-facing key. The hook output must not overwrite a value the caller already passed.
    result = compose_method_params(
        params,
        update,
        default_params={"direct_messages_topic"},
        hooks={"direct_messages_topic": lambda field: ("direct_messages_topic_id", field)},
    )
    # Buggy behaviour clobbered the caller's 999 with the incoming message's value.
    assert result["direct_messages_topic_id"] == 999


def test_message_unixtime_reads_the_unix_time_entity(message_update, api_instance):
    from telegrinder.bot.cute_types.message import MessageCute

    msg = MessageCute.from_update(message_update.message.unwrap(), bound_api=api_instance)
    entity = MessageEntity.from_raw(b'{"type": "code", "offset": 0, "length": 1}')
    object.__setattr__(entity, "unix_time", 1700000000)
    object.__setattr__(msg, "entities", Some([entity]))

    # The property queried the non-existent attribute "unixtime" (always NOTHING) before the fix.
    assert msg.unixtime.unwrap() == 1700000000


def test_token_repr_does_not_leak_the_secret():
    token = Token("123:SUPERSECRETTOKENVALUE")
    representation = repr(token)
    # No prefix of the secret may appear (the old repr exposed the first nine characters).
    assert all(token.token[:n] not in representation for n in range(4, len(token.token) + 1))
    assert "SECRET" not in representation
    assert "123" in representation


# --------------------------------------------------------------------------- global context


def test_global_context_copy_is_an_independent_snapshot():
    class _NamedContext(GlobalContext):
        __ctx_name__ = "regression_copy_ctx"

    original = _NamedContext()
    original["value"] = 1
    copied = original.copy()

    # copy() routed through __new__, which returned the same singleton instance.
    assert copied is not original
    # It must be an independent, anonymous snapshot (not aliasing the original's storage).
    assert copied.__ctx_name__ is None
    assert copied["value"] == 1
    copied["value"] = 2
    assert original["value"] == 1


def test_global_context_equality_does_not_recurse():
    ctx = GlobalContext("regression_eq_ctx", value=1)
    same = GlobalContext("regression_eq_ctx")  # same name -> same singleton instance
    # `self == __value` re-entered __eq__ and raised RecursionError.
    assert ctx == same


def test_global_context_rename_missing_returns_error():
    ctx = GlobalContext("regression_rename_ctx", existing=1)
    # Renaming a missing variable raised UnwrapError instead of returning an Error result.
    assert not ctx.rename("missing", "new")


def test_global_context_missing_attribute_raises_attribute_error():
    ctx = GlobalContext("regression_getattr_ctx", existing=1)
    # hasattr() raised UnwrapError (a BaseException) instead of returning False.
    assert hasattr(ctx, "missing") is False
    assert getattr(ctx, "missing", "default") == "default"


def test_global_context_update_enforces_const():
    a = GlobalContext("regression_update_a")
    a.host = CtxVar("1.1.1.1", const=True)
    b = GlobalContext("regression_update_b", host="9.9.9.9")
    # update() bypassed const protection and silently overwrote the constant.
    with pytest.raises(TypeError):
        a.update(b)


# --------------------------------------------------------------------------- formatting (HTML & deep links)


def test_link_escapes_its_href_attribute():
    result = link('a"b', text="x").formatting()
    # A raw double-quote broke out of the href attribute.
    assert "&quot;" in result
    assert 'href="a"b"' not in result


def test_tg_emoji_and_date_time_escape_attribute_values():
    # Each helper independently interpolates its attribute; all must escape.
    assert "&quot;" in tg_emoji("x", emoji_id='5"evil').formatting()
    assert "&quot;" in date_time("x", 1700000000, format='%Y"evil').formatting()


def test_pre_code_quotes_and_escapes_its_class_attribute():
    # pre_code was the one helper whose `class` value was unquoted: a space in `lang` would inject
    # a standalone attribute. The value must be wrapped in quotes, like the other helpers.
    result = pre_code("x", lang="py onmouseover=alert").formatting()
    assert 'class="language-py onmouseover=alert"' in result
    assert "&quot;" in pre_code("x", lang='py"evil').formatting()


def test_template_format_spec_escapes_exactly_once():
    name = "&"
    # The value was escaped before AND inside the formatter, producing `&amp;amp;`.
    assert escape(t"{name:bold}") == "<b>&amp;</b>"


def test_tag_attributes_are_not_comma_separated():
    result = date_time("label", 1700000000, format="%Y").formatting()
    # Multiple attributes were joined with a comma, producing invalid HTML.
    assert "," not in result
    assert 'unix="1700000000" format="%Y"' in result


def test_parse_query_params_keeps_integer_zero_and_one():
    no_value, params = parse_query_params(
        {"a": 0, "b": 1, "c": 5, "flag": True, "off": False, "skip": NO_VALUE},
    )
    # `0 == False` dropped `a`, and `1 == True` turned `b` into a value-less flag.
    assert params == {"a": 0, "b": 1, "c": 5}
    # Genuine bool flags / NO_VALUE still become value-less params; False is still dropped.
    assert no_value == {"flag", "skip"}


# --------------------------------------------------------------------------- serialization


def test_msgpack_deserialize_returns_error_on_malformed_data():
    class _Model(msgspec.Struct):
        a: int
        b: int

    ser = MsgPackSerializer(_Model)
    encoded = ser.key + msgspec.msgpack.encode([1])  # one element, model needs two
    if msgpack_ser.brotli is not None:
        payload = base64.b85encode(msgpack_ser.brotli.compress(encoded, quality=11)).decode()
    else:
        payload = base64.urlsafe_b64encode(encoded).decode()

    # compose() raised IndexError on attacker bytes, escaping the Result boundary.
    result = ser.deserialize(payload)
    assert not result


def test_json_serializer_deserializes_default_dict_model():
    # The default model type is the generic alias dict[str, typing.Any]; pass it explicitly so the
    # parameterized generic still flows through deserialize's issubclass check (the regression site).
    ser = JSONSerializer(dict[str, typing.Any])
    serialized = ser.serialize({"a": 1})
    # issubclass(dict[str, Any], dict) raised TypeError on the parameterized generic.
    result = ser.deserialize(serialized)
    assert result.unwrap() == {"a": 1}


# --------------------------------------------------------------------------- waiter machine & state


@pytest.mark.asyncio()
async def test_waiter_drop_passes_state_to_plain_on_drop_callback():
    wm = WaiterMachine()
    hasher = Hasher(update_types=frozenset({UpdateType.MESSAGE}), hash_from_data=lambda data: data)
    wm.storage[hasher] = LimitedDict(maxlimit=100)

    captured: list[tuple] = []

    async def on_drop(short_state, foo):  # plain function: first param must survive bundling
        captured.append((short_state, foo))

    short_state = ShortState({"on_drop": on_drop}, expiration=datetime.timedelta(seconds=10))
    wm.storage[hasher].set("key", short_state)

    # Bundling stripped `short_state` (default start_idx=1), raising TypeError on the callback.
    await wm.drop(hasher, "key", foo="bar")
    assert captured == [(short_state, "bar")]


@pytest.mark.asyncio()
async def test_waiter_lifetime_expiry_releases_instead_of_cancelling():
    wm = WaiterMachine()
    hasher = Hasher(update_types=frozenset({UpdateType.MESSAGE}), hash_from_data=lambda data: data)
    wm.storage[hasher] = LimitedDict(maxlimit=100)

    short_state = ShortState({}, expiration=datetime.timedelta(seconds=10))
    wm.storage[hasher].set("key", short_state)

    # Mimic acquire(): a coroutine suspended on the short_state's event.
    waiter = asyncio.create_task(short_state.event.wait())
    await asyncio.sleep(0)

    # On expiry the waiter must be woken gracefully (release), not have its future cancelled.
    await wm.drop(hasher, "key", expired=True)
    await asyncio.sleep(0)

    assert waiter.done()
    # Buggy behaviour always called cancel(), surfacing an uncatchable CancelledError to the caller.
    assert not waiter.cancelled()
    assert waiter.result() is True


def test_limited_dict_reset_at_capacity_keeps_other_entries():
    d = LimitedDict(maxlimit=3)
    d.set("a", 1)
    d.set("b", 2)
    d.set("c", 3)

    deleted = d.set("b", 22)  # re-set an existing key while at capacity
    # Buggy behaviour evicted an unrelated entry ("a") and returned it.
    assert deleted is None
    assert set(d.keys()) == {"a", "b", "c"}
    assert d["b"] == 22


# --------------------------------------------------------------------------- lifespan & async


@pytest.mark.asyncio()
async def test_lifespan_run_coro_tasks_survives_a_failing_task():
    async def bad(_: _FailingNode) -> None: ...

    # The error branch popped the (now empty) task list again, raising IndexError.
    await Lifespan._run_coro_task_functions([bad])


def test_lifespan_add_preserves_decorator_registered_tasks():
    a = Lifespan()
    b = Lifespan()

    async def hook() -> None: ...

    b.on_shutdown(hook)
    combined = a + b
    # __add__ only copied startup_tasks/shutdown_tasks, dropping decorator-registered functions.
    assert hook in combined.shutdown_coro_task_functions


def test_lifespan_iadd_preserves_decorator_registered_tasks():
    a = Lifespan()
    b = Lifespan()

    async def hook() -> None: ...

    b.on_startup(hook)
    a += b
    assert hook in a.startup_coro_task_functions


def test_lifespan_add_preserves_lifespan_function():
    a = Lifespan()
    b = Lifespan()

    @b
    async def lifespan_fn():
        yield

    combined = a + b
    # __add__ rebuilt from only the startup/shutdown task lists, dropping the lifespan function.
    assert combined.lifespan_function is b.lifespan_function


@pytest.mark.asyncio()
async def test_taskgroup_create_task_forwards_name():
    async def coro() -> int:
        return 1

    async with TaskGroup() as tg:
        task = tg.create_task(coro(), name="my-task")
        # name/context were dropped, so the task got a default name.
        assert task.get_name() == "my-task"


# --------------------------------------------------------------------------- polling & API


@pytest.mark.asyncio()
async def test_retryer_writes_migrated_chat_id_into_payload():
    calls: list[tuple[dict | None, dict]] = []

    class _FakeAPI:
        retryer_is_enabled = True
        max_retries = 3

    @retryer
    async def fake_request(self, method, data=None, **kwargs):
        calls.append((None if data is None else dict(data), dict(kwargs)))
        if len(calls) == 1:
            return Error(APIError(code=400, error="migrate", data={"migrate_to_chat_id": 999}))
        return Ok("done")

    result = await fake_request(_FakeAPI(), "sendMessage", {"chat_id": 111, "text": "hi"})

    assert result
    assert len(calls) == 2
    retried_data, retried_kwargs = calls[1]
    assert retried_data is not None
    # The new chat id was written to **kwargs and never reached the request payload.
    assert retried_data["chat_id"] == 999
    assert "chat_id" not in retried_kwargs


@pytest.mark.asyncio()
async def test_error_handler_reraises_system_exit():
    api = API(Token("123:ABCdef"), http=MockedHttpClient())
    handler = ErrorHandler(Polling(api))
    # _handle_system_exit was created as a coroutine but never awaited, so it never raised.
    with pytest.raises(SystemExit):
        await handler.handle(SystemExit(5))


@pytest.mark.asyncio()
async def test_polling_listen_keeps_a_reference_to_the_stop_task():
    api = API(Token("123:ABCdef"), http=MockedHttpClient())
    polling = Polling(api)
    generator = polling.listen()
    try:
        # The stop task used to be fire-and-forget; there was no _stop_task slot/attribute at all.
        assert polling._stop_task is not None
        polling.stop()
        await asyncio.gather(polling._stop_task, return_exceptions=True)
    finally:
        await generator.aclose()


def test_reconnect_limit_comparison_is_inclusive():
    src = (REPO_ROOT / "telegrinder/bot/polling/error_handler.py").read_text()
    # The comparison used `>` and so allowed one reconnect past the configured limit.
    assert "self._polling.reconnects_counter >= self._polling.max_reconnects" in src


@pytest.mark.asyncio()
@with_mocked_api({"ok": True})
async def test_request_returns_ok_none_when_result_missing(api: API):
    # response["result"] raised KeyError when the response was ok but carried no result.
    result = await api.request("getMe")
    assert result
    assert result.unwrap() is None


# --------------------------------------------------------------------------- HTTP client


@pytest.mark.asyncio()
async def test_wreq_client_close_closes_the_underlying_client():
    client = WreqClient()
    closed: list[bool] = []

    class _FakeClient:
        def close(self) -> None:
            closed.append(True)

    # _client holds a native wreq.Client; inject a stand-in to observe the delegated close().
    object.__setattr__(client, "_client", _FakeClient())
    await client.close()
    # close() was a no-op and never released the connection pool.
    assert closed == [True]


def test_wreq_request_methods_accept_positional_url():
    for name in ("request_text", "request_bytes", "request_content", "request_json"):
        code = vars(WreqClient)[name].__code__
        positional = code.co_varnames[: code.co_argcount]
        # url was keyword-only (after `*`), unlike ABCClient which declares it positional-or-keyword.
        assert "url" in positional, name


# --------------------------------------------------------------------------- node composition


@pytest.mark.asyncio()
async def test_global_scope_close_waiter_is_kept_referenced(monkeypatch):
    import sys

    import telegrinder.node.compose  # noqa: F401  (ensure the submodule is imported)

    # `telegrinder.node.compose` the attribute is the compose() function (re-exported by the
    # package), so fetch the actual module object from sys.modules.
    compose_mod = sys.modules["telegrinder.node.compose"]

    async def _noop() -> None:
        return None

    # Use a no-op waiter (the real one closes the global node scope on cancel) and bypass the
    # lru_cache via __wrapped__ so we neither clear the cache nor release the real cached task
    # (clearing it would let that task get GC'd and close the scope — the very bug under test).
    monkeypatch.setattr(compose_mod, "wait_for_close_node_global_scope", _noop)
    result = compose_mod._register_waiter_close_node_global_scope.__wrapped__()
    # The waiter task used to be discarded (returned None) and was thus GC-collectable.
    assert isinstance(result, asyncio.Task)
    await result


def test_managed_bot_username_node_uses_expect():
    src = (REPO_ROOT / "telegrinder/node/nodes/managed_bot.py").read_text()
    assert "managed_bot_created_bot.username.unwrap()" not in src
    assert 'managed_bot_created_bot.username.expect(NodeError("Managed bot has no username."))' in src


def test_managed_bot_username_node_raises_catchable_node_error():
    class _BotWithoutUsername:
        username = Nothing()

    # The real issue is catchability: `.unwrap()` raises a bare UnwrapError (not a NodeError) that
    # escapes the `except NodeError` compose boundary; `.expect(NodeError(...))` stays catchable.
    # `@scalar_node` types the node as its scalar value (str), erasing __compose__ from the static
    # type, so reach the classmethod through an untyped handle to drive it with a stub bot.
    node: typing.Any = ManagedBotCreatedBotUsername
    with pytest.raises(NodeError):
        node.__compose__(_BotWithoutUsername())


def test_get_types_raises_on_unrecognized_annotation():
    import threading

    outcome: dict[str, object] = {}

    def run() -> None:
        try:
            _get_types(object())
        except TypeError:
            outcome["raised"] = True

    thread = threading.Thread(target=run, daemon=True)
    thread.start()
    thread.join(timeout=3.0)

    # _get_types used to spin forever on an unrecognized annotation.
    assert not thread.is_alive(), "_get_types did not terminate"
    assert outcome.get("raised") is True


# --------------------------------------------------------------------------- introspection & tools


def test_resolve_kwonly_arg_names_includes_first_kwonly():
    def g(a, b, *, kw1, kw2): ...

    # An off-by-one dropped the first keyword-only argument (returned only ("kw2",)).
    assert resolve_kwonly_arg_names(g) == ("kw1", "kw2")

    def h(*, only): ...

    assert resolve_kwonly_arg_names(h) == ("only",)


def test_generic_parameters_resolves_non_leading_typevartuple():
    values = list(get_generic_parameters(_Generic[int, str, bytes]).unwrap().values())
    # The TypeVarTuple absorbed the wrong slice (only (str,) instead of (str, bytes)).
    assert int in values
    assert (str, bytes) in values


def test_keyboard_format_text_returns_independent_copy():
    kb = InlineKeyboard().add(InlineButton("Hi {name}", callback_data="x"))

    first = kb.format_text(name="Bob")
    second = kb.format_text(name="Alice")

    assert first.keyboard[0][0]["text"] == "Hi Bob"
    # The original template was consumed on the first call, so the second one was wrong.
    assert second.keyboard[0][0]["text"] == "Hi Alice"
    assert kb.keyboard[0][0]["text"] == "Hi {name}"


def test_singleton_metaclass_uses_a_lock():
    # Use a throwaway subclass: instantiating the base Singleton would set the shared
    # `_SingletonMeta__instance` that real singleton subclasses (e.g. MiddlewareBox) inherit.
    class _MySingleton(Singleton):
        pass

    assert _MySingleton() is _MySingleton()
    # The metaclass had no lock, so check-then-create was a TOCTOU race.
    assert hasattr(SingletonMeta, "_SingletonMeta__lock")


@pytest.mark.asyncio()
async def test_memory_state_storage_delete_is_idempotent():
    storage = MemoryStateStorage()
    # Deleting an unknown user used to raise KeyError.
    await storage.delete(123456)


def test_mutation_descriptor_binds_state_independently_per_access():
    class _MutState(State):
        pass

    async def _construct(*args, **kwargs):
        return _MutState()

    m = mutation(_construct)

    a, b = _MutState(), _MutState()
    bound_a = m.__get__(a, _MutState)
    bound_b = m.__get__(b, _MutState)

    # __get__ used to stash `from_state` on the single shared descriptor and return it, so the
    # second access clobbered the first (cross-user state corruption under concurrency).
    assert bound_a is not bound_b
    assert bound_b.from_state is b
    assert bound_a.from_state is a


def test_logger_proxy_tolerates_logger_without_isenabledfor():
    from telegrinder.modules import _LoggerProxy

    class _Dummy:
        def debug(self, *args, **kwargs) -> None:
            return None

    # A fresh proxy (not the global singleton) so the test does not pollute logging for others.
    proxy = _LoggerProxy()
    # logger is typed as the configured-logger union; inject a minimal duck-typed logger directly.
    object.__setattr__(proxy, "logger", _Dummy())
    proxy.logger_module = "logging"
    # An inverted boolean called isEnabledFor on a logger that does not define it.
    assert callable(proxy.debug)
