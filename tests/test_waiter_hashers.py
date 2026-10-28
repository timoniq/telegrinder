import asyncio
import copy

import msgspec
import pytest

from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.cute_types.stopped_message_generation import MessageGenerationStoppedCute
from telegrinder.bot.cute_types.update import UpdateCute
from telegrinder.bot.dispatch.dispatch import Dispatch
from telegrinder.bot.dispatch.middleware.waiter import WaiterMiddleware
from telegrinder.tools.lifespan import Lifespan
from telegrinder.tools.waiter_machine import WaiterMachine
from telegrinder.tools.waiter_machine import hasher as hashers


def waiter_update_payloads():
    user = {"id": 11, "is_bot": False, "first_name": "User"}
    actor = {"id": 21, "is_bot": False, "first_name": "Actor"}
    target = {"id": 31, "is_bot": False, "first_name": "Target"}
    receiver = {"id": 41, "is_bot": False, "first_name": "Receiver"}
    bot = {"id": 51, "is_bot": True, "first_name": "Bot"}
    chat = {"id": -100, "type": "supergroup"}
    message = {
        "message_id": 23,
        "date": 1,
        "chat": chat,
        "from": user,
        "message_thread_id": 17,
        "sender_chat": {"id": -200, "type": "channel"},
        "sender_business_bot": bot,
        "via_bot": bot,
        "receiver_user": receiver,
        "ephemeral_message_id": 29,
        "business_connection_id": "connection_a",
        "guest_query_id": "guest_a",
        "media_group_id": "album_a",
        "direct_messages_topic": {"topic_id": 19, "user": user},
    }
    member = {
        "chat": chat,
        "from": actor,
        "date": 1,
        "old_chat_member": {"status": "left", "user": target},
        "new_chat_member": {"status": "member", "user": target},
    }
    source = {"source": "premium", "user": user}
    address = dict(country_code="US", state="", city="City", street_line1="Street", street_line2="", post_code="123")
    return {
        **{
            name: copy.deepcopy(message)
            for name in (
                "message",
                "edited_message",
                "channel_post",
                "edited_channel_post",
                "business_message",
                "edited_business_message",
                "guest_message",
            )
        },
        "business_connection": {"id": "connection_a", "user": user, "user_chat_id": 777, "date": 1, "is_enabled": True},
        "deleted_business_messages": {"business_connection_id": "connection_a", "chat": chat, "message_ids": [23, 24]},
        "message_reaction": {
            "chat": chat,
            "message_id": 23,
            "date": 1,
            "user": user,
            "old_reaction": [],
            "new_reaction": [{"type": "emoji", "emoji": "👍"}],
        },
        "message_reaction_count": {"chat": chat, "message_id": 23, "date": 1, "reactions": []},
        "inline_query": {"id": "query_a", "from": user, "query": "text", "offset": ""},
        "chosen_inline_result": {
            "result_id": "result_a",
            "from": user,
            "query": "text",
            "inline_message_id": "inline_a",
        },
        "callback_query": {
            "id": "query_a",
            "from": user,
            "chat_instance": "instance_a",
            "message": message,
            "data": "button_a",
        },
        "shipping_query": {"id": "query_a", "from": user, "invoice_payload": "invoice_a", "shipping_address": address},
        "pre_checkout_query": {
            "id": "query_a",
            "from": user,
            "currency": "XTR",
            "total_amount": 1,
            "invoice_payload": "invoice_a",
            "shipping_option_id": "shipping_a",
        },
        "purchased_paid_media": {"from": user, "paid_media_payload": "media_a"},
        "poll": {
            "id": "poll_a",
            "question": "Question",
            "options": [],
            "total_voter_count": 0,
            "is_closed": False,
            "is_anonymous": False,
            "allows_multiple_answers": False,
            "allows_revoting": True,
            "members_only": False,
            "type": "regular",
        },
        "poll_answer": {"poll_id": "poll_a", "option_ids": [0], "option_persistent_ids": ["option_a"], "user": user},
        "my_chat_member": copy.deepcopy(member),
        "chat_member": member,
        "chat_join_request": {"chat": chat, "from": user, "user_chat_id": 777, "date": 1, "query_id": "join_a"},
        "chat_boost": {
            "chat": chat,
            "boost": {"boost_id": "boost_a", "add_date": 1, "expiration_date": 2, "source": source},
        },
        "removed_chat_boost": {"chat": chat, "boost_id": "boost_a", "remove_date": 2, "source": source},
        "managed_bot": {"user": user, "bot": bot},
        "subscription": {"user": user, "invoice_payload": "invoice_a", "state": "active"},
        "stopped_message_generation": {"chat": chat, "draft_id": 25, "message_thread_id": 17},
    }


def make_update(api, kind, payload):
    return UpdateCute.from_raw(msgspec.json.encode({"update_id": 1, kind: payload}), api)


async def start_waiter(machine, middleware, hasher, key):
    started = asyncio.Event()

    async def ready():
        started.set()

    task = asyncio.create_task(
        machine.wait_many(
            hasher(key),
            waiter_middleware=middleware,
            lifetime=30,
            lifespan=Lifespan(startup_tasks=[ready()]),
        )
    )
    await asyncio.wait_for(started.wait(), timeout=1)
    return task


async def feed_waiter(api, middleware, kind, payload):
    update = make_update(api, kind, payload)
    async with Dispatch._create_update_context(api, update) as context:
        return await middleware.pre(api, context)


@pytest.mark.asyncio()
async def test_callback_waiters_are_scoped_by_chat_message_and_user(api_instance):
    machine = WaiterMachine()
    middleware = WaiterMiddleware(machine)
    hasher = hashers.CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE_FROM_USER
    first = await start_waiter(machine, middleware, hasher, (-100, 23, 11))
    second = await start_waiter(machine, middleware, hasher, (-200, 23, 11))
    payload = waiter_update_payloads()["callback_query"]
    try:
        wrong_user = copy.deepcopy(payload)
        wrong_user["from"]["id"] = 12
        assert await feed_waiter(api_instance, middleware, "callback_query", wrong_user) is True
        wrong_message = copy.deepcopy(payload)
        wrong_message["message"]["message_id"] = 24
        assert await feed_waiter(api_instance, middleware, "callback_query", wrong_message) is True
        assert not first.done() and not second.done()

        assert await feed_waiter(api_instance, middleware, "callback_query", payload) is False
        _, event, _ = await asyncio.wait_for(first, timeout=1)
        assert event.chat_id.unwrap() == -100
        assert event.from_user.id == 11
        assert not second.done()

        payload["message"]["chat"]["id"] = -200
        assert await feed_waiter(api_instance, middleware, "callback_query", payload) is False
        _, event, _ = await asyncio.wait_for(second, timeout=1)
        assert event.chat_id.unwrap() == -200
    finally:
        first.cancel()
        second.cancel()
        await asyncio.gather(first, second, return_exceptions=True)


@pytest.mark.asyncio()
async def test_string_pair_keys_do_not_replace_a_different_waiter(api_instance):
    machine = WaiterMachine()
    middleware = WaiterMiddleware(machine)
    hasher = hashers.PRE_CHECKOUT_QUERY_FOR_PAYLOAD_AND_SHIPPING_OPTION
    first = await start_waiter(machine, middleware, hasher, ("a_b", "c"))
    second = await start_waiter(machine, middleware, hasher, ("a", "b_c"))
    payload = waiter_update_payloads()["pre_checkout_query"]
    try:
        payload.update(invoice_payload="a_b", shipping_option_id="c")
        assert await feed_waiter(api_instance, middleware, "pre_checkout_query", payload) is False
        _, event, _ = await asyncio.wait_for(first, timeout=1)
        assert event.invoice_payload == "a_b"
        assert not second.done()
        payload.update(invoice_payload="a", shipping_option_id="b_c")
        assert await feed_waiter(api_instance, middleware, "pre_checkout_query", payload) is False
        _, event, _ = await asyncio.wait_for(second, timeout=1)
        assert event.shipping_option_id.unwrap() == "b_c"
    finally:
        first.cancel()
        second.cancel()
        await asyncio.gather(first, second, return_exceptions=True)


@pytest.mark.asyncio()
async def test_deleted_business_batch_does_not_enter_message_extractors(api_instance):
    machine = WaiterMachine()
    middleware = WaiterMiddleware(machine)
    message_waiter = await start_waiter(machine, middleware, hashers.ANY_MESSAGE_FROM_USER, 11)
    tasks = [message_waiter]
    try:
        payload = waiter_update_payloads()["deleted_business_messages"]
        assert await feed_waiter(api_instance, middleware, "deleted_business_messages", payload) is True
        assert not message_waiter.done()
        deletion_waiter = await start_waiter(
            machine,
            middleware,
            hashers.DELETED_BUSINESS_MESSAGES_IN_CHAT_FOR_CONNECTION,
            ("connection_a", -100),
        )
        tasks.append(deletion_waiter)
        assert await feed_waiter(api_instance, middleware, "deleted_business_messages", payload) is False
        _, event, _ = await asyncio.wait_for(deletion_waiter, timeout=1)
        assert event.message_ids == [23, 24]
        assert not message_waiter.done()
    finally:
        for task in tasks:
            task.cancel()
        await asyncio.gather(*tasks, return_exceptions=True)


@pytest.mark.parametrize("kind", ["message", "guest_message"])
def test_private_thread_key_uses_sender_not_chat(api_instance, kind):
    payload = waiter_update_payloads()[kind]
    payload["chat"] = {"id": 101, "type": "private"}
    event = make_update(api_instance, kind, payload).incoming_update
    assert isinstance(event, MessageCute)
    hasher = hashers.MESSAGE_FROM_USER_IN_THREAD if kind == "message" else hashers.GUEST_MESSAGE_FROM_USER_IN_THREAD
    assert hasher.get_data_from_event(event).unwrap() == (17, 11)


@pytest.mark.parametrize("kind", ["chat_member", "my_chat_member"])
def test_member_actor_is_distinct_from_target(api_instance, kind):
    event = make_update(api_instance, kind, waiter_update_payloads()[kind]).incoming_update
    prefix = kind.upper()
    assert getattr(hashers, prefix + "_FROM_USER_IN_CHAT").get_data_from_event(event).unwrap() == (-100, 21)
    assert getattr(hashers, prefix + "_FOR_USER_IN_CHAT").get_data_from_event(event).unwrap() == (-100, 31)


@pytest.mark.parametrize("kind", ["poll_answer", "message_reaction"])
def test_optional_user_and_chat_actors_are_not_conflated(api_instance, kind):
    payload = waiter_update_payloads()[kind]
    payload.pop("user")
    chat_field = "voter_chat" if kind == "poll_answer" else "actor_chat"
    payload[chat_field] = {"id": -200, "type": "channel"}
    event = make_update(api_instance, kind, payload).incoming_update
    user_hasher = getattr(hashers, kind.upper() + "_FROM_USER")
    chat_hasher = getattr(hashers, kind.upper() + ("_FROM_CHAT" if kind == "poll_answer" else "_FROM_ACTOR_CHAT"))
    assert user_hasher.get_hash_from_data_from_event(event).unwrap_or_none() is None
    assert chat_hasher.get_data_from_event(event).unwrap() == -200

    payload.pop(chat_field)
    payload["user"] = {"id": 0, "is_bot": False, "first_name": "Zero"}
    event = make_update(api_instance, kind, payload).incoming_update
    assert user_hasher.get_data_from_event(event).unwrap() == 0
    assert chat_hasher.get_hash_from_data_from_event(event).unwrap_or_none() is None


@pytest.mark.parametrize("kind", ["chat_boost", "removed_chat_boost"])
@pytest.mark.parametrize("source_kind", ["premium", "gift_code", "giveaway"])
def test_boost_source_variants_and_unclaimed_giveaways(api_instance, kind, source_kind):
    payload = waiter_update_payloads()[kind]
    source = {"source": source_kind, "user": {"id": 0, "is_bot": False, "first_name": "Zero"}}
    if source_kind == "giveaway":
        source["giveaway_message_id"] = 43
    if kind == "chat_boost":
        payload["boost"]["source"] = source
    else:
        payload["source"] = source
    prefix = kind.upper()
    user_hasher = getattr(hashers, prefix + "_FROM_USER_IN_CHAT")
    giveaway_hasher = getattr(hashers, prefix + "_IN_CHAT_FOR_GIVEAWAY")
    event = make_update(api_instance, kind, payload).incoming_update
    assert user_hasher.get_data_from_event(event).unwrap() == (-100, 0)
    if source_kind == "giveaway":
        assert giveaway_hasher.get_data_from_event(event).unwrap() == (-100, 43)
        source.pop("user")
        event = make_update(api_instance, kind, payload).incoming_update
        assert user_hasher.get_hash_from_data_from_event(event).unwrap_or_none() is None
        assert giveaway_hasher.get_data_from_event(event).unwrap() == (-100, 43)
    else:
        assert giveaway_hasher.get_hash_from_data_from_event(event).unwrap_or_none() is None


def test_inline_callback_has_no_chat_or_ordinary_message_key(api_instance):
    payload = waiter_update_payloads()["callback_query"]
    payload.pop("message")
    payload["inline_message_id"] = "inline_a"
    event = make_update(api_instance, "callback_query", payload).incoming_update
    assert isinstance(event, CallbackQueryCute)
    assert (
        hashers.CALLBACK_QUERY_IN_CHAT_FOR_MESSAGE_FROM_USER.get_hash_from_data_from_event(event).unwrap_or_none()
        is None
    )
    assert hashers.CALLBACK_QUERY_FOR_INLINE_MESSAGE_FROM_USER.get_data_from_event(event).unwrap() == ("inline_a", 11)
    assert hashers.CALLBACK_QUERY_FROM_USER_IN_CHAT_INSTANCE.get_data_from_event(event).unwrap() == ("instance_a", 11)


def test_ephemeral_ids_and_receiver_are_distinct_from_sender(api_instance):
    payload = waiter_update_payloads()["message"]
    payload["message_id"] = 0
    payload["ephemeral_message_id"] = 0
    event = make_update(api_instance, "message", payload).incoming_update
    assert isinstance(event, MessageCute)
    assert hashers.MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE_FOR_USER.get_data_from_event(event).unwrap() == (-100, 0, 41)
    assert hashers.MESSAGE_FROM_USER.get_data_from_event(event).unwrap() == 11
    payload.pop("ephemeral_message_id")
    event = make_update(api_instance, "message", payload).incoming_update
    assert isinstance(event, MessageCute)
    assert hashers.MESSAGE_IN_CHAT_FOR_EPHEMERAL_MESSAGE.get_hash_from_data_from_event(event).unwrap_or_none() is None


def test_business_message_keys_include_connection_namespace(api_instance):
    payload = waiter_update_payloads()["business_message"]
    hasher = hashers.BUSINESS_MESSAGE_FOR_CONNECTION_IN_CHAT_FOR_MESSAGE
    first = make_update(api_instance, "business_message", payload).incoming_update
    payload["business_connection_id"] = "connection_b"
    second = make_update(api_instance, "business_message", payload).incoming_update

    assert isinstance(first, MessageCute)
    assert isinstance(second, MessageCute)
    assert hasher.get_data_from_event(first).unwrap() == ("connection_a", -100, 23)
    assert hasher.get_hash_from_data_from_event(first) != hasher.get_hash_from_data_from_event(second)


def test_stopped_generation_requires_thread_for_thread_scoped_keys(api_instance):
    payload = waiter_update_payloads()["stopped_message_generation"]
    payload.pop("message_thread_id")
    event = make_update(api_instance, "stopped_message_generation", payload).incoming_update

    assert isinstance(event, MessageGenerationStoppedCute)
    assert hashers.MESSAGE_GENERATION_STOPPED_IN_CHAT_FOR_DRAFT.get_data_from_event(event).unwrap() == (-100, 25)
    assert (
        hashers.MESSAGE_GENERATION_STOPPED_IN_CHAT_THREAD_FOR_DRAFT.get_hash_from_data_from_event(
            event
        ).unwrap_or_none()
        is None
    )


@pytest.mark.asyncio()
async def test_cute_callback_ephemeral_waiter_uses_actor_not_receiver(api_instance):
    payload = waiter_update_payloads()["callback_query"]
    event = make_update(api_instance, "callback_query", payload).incoming_update

    assert isinstance(event, CallbackQueryCute)

    machine = WaiterMachine()
    middleware = WaiterMiddleware(machine)
    hasher, key = event.IN_CHAT_FOR_EPHEMERAL_MESSAGE_FROM_USER()
    task = await start_waiter(machine, middleware, hasher, key)

    try:
        wrong_actor = copy.deepcopy(payload)
        wrong_actor["from"]["id"] = payload["message"]["receiver_user"]["id"]
        assert await feed_waiter(api_instance, middleware, "callback_query", wrong_actor) is True
        assert not task.done()

        assert await feed_waiter(api_instance, middleware, "callback_query", payload) is False
        _, received, _ = await asyncio.wait_for(task, timeout=1)
        assert received.from_user.id == 11
        assert received.ephemeral_message_id.unwrap() == 29
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio()
async def test_cute_callback_overrides_bypass_missing_message_and_preserve_zero(api_instance):
    source = waiter_update_payloads()["callback_query"]
    source.pop("message")
    source["inline_message_id"] = "inline_a"
    event = make_update(api_instance, "callback_query", source).incoming_update

    assert isinstance(event, CallbackQueryCute)

    with pytest.raises(ValueError):
        event.IN_CHAT_FOR_EPHEMERAL_MESSAGE_FROM_USER(chat_id=0)

    machine = WaiterMachine()
    middleware = WaiterMiddleware(machine)
    hasher, key = event.IN_CHAT_FOR_EPHEMERAL_MESSAGE_FROM_USER(
        chat_id=0,
        ephemeral_message_id=0,
        user_id=0,
    )
    task = await start_waiter(machine, middleware, hasher, key)

    try:
        payload = waiter_update_payloads()["callback_query"]
        payload["from"]["id"] = 0
        payload["message"]["chat"]["id"] = 0
        payload["message"]["ephemeral_message_id"] = 1
        assert await feed_waiter(api_instance, middleware, "callback_query", payload) is True
        assert not task.done()

        payload["message"]["ephemeral_message_id"] = 0
        assert await feed_waiter(api_instance, middleware, "callback_query", payload) is False
        _, received, _ = await asyncio.wait_for(task, timeout=1)
        assert received.from_user.id == 0
        assert received.chat_id.unwrap() == 0
        assert received.ephemeral_message_id.unwrap() == 0
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)


@pytest.mark.asyncio()
@pytest.mark.parametrize("kind", ["chat_boost", "removed_chat_boost"])
async def test_cute_unclaimed_boost_can_wait_for_an_explicit_zero_user(api_instance, kind):
    payload = waiter_update_payloads()[kind]
    source_parent = payload["boost"] if kind == "chat_boost" else payload
    source_parent["source"] = {"source": "giveaway", "giveaway_message_id": 0}
    event = make_update(api_instance, kind, payload).incoming_update

    with pytest.raises(ValueError):
        getattr(event, "FROM_USER_IN_CHAT")()

    with pytest.raises(ValueError):
        getattr(event, "FROM_USER_IN_CHAT")(chat_id=0)

    machine = WaiterMachine()
    middleware = WaiterMiddleware(machine)
    hasher, key = getattr(event, "FROM_USER_IN_CHAT")(user_id=0)
    task = await start_waiter(machine, middleware, hasher, key)

    try:
        assert await feed_waiter(api_instance, middleware, kind, payload) is True
        assert not task.done()

        source_parent["source"]["user"] = {"id": 0, "is_bot": False, "first_name": "Zero"}
        assert await feed_waiter(api_instance, middleware, kind, payload) is False
        _, received, _ = await asyncio.wait_for(task, timeout=1)
        received_source = received.boost.source.v if kind == "chat_boost" else received.source.v
        assert received_source.user.unwrap().id == 0
    finally:
        task.cancel()
        await asyncio.gather(task, return_exceptions=True)
