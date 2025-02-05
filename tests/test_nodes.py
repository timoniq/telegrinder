import dataclasses
import typing

import pytest

from telegrinder.api.api import API
from telegrinder.bot.cute_types.callback_query import CallbackQueryCute
from telegrinder.bot.cute_types.message import MessageCute
from telegrinder.bot.dispatch.context import Context
from telegrinder.bot.rules import IsUser, Markup
from telegrinder.node import DataNode, Node, Polymorphic, impl, scalar_node
from telegrinder.node.base import ComposeError
from telegrinder.node.callback_query import CallbackQueryNode
from telegrinder.node.composer import NodeCollection, compose_nodes
from telegrinder.node.event import EventNode
from telegrinder.node.me import Me
from telegrinder.node.message import MessageNode
from telegrinder.node.rule import RuleChain
from telegrinder.node.text import Text
from telegrinder.node.tools.generator import generate_node
from telegrinder.node.update import UpdateNode
from telegrinder.types.objects import Message, Update, User
from tests.test_utils import with_mocked_api

GET_ME_RAW_RESPONSE = """
{
  "ok": true,
  "result": {
    "id": 55732494,
    "is_bot": true,
    "first_name": "Cute",
    "username": "cute123_bot",
    "can_join_groups": true,
    "can_read_all_group_messages": false,
    "supports_inline_queries": true
  }
}
"""


class PrettyRuleChain(
    RuleChain[
        Markup("Hello, <framework>! btw, <logical_lang> - nice pure logical programming launguage <smile>"),
        IsUser(),
    ]
):
    framework: str
    logical_lang: str
    smile: str


@scalar_node(int)
class ScalarMorphNode(Polymorphic):
    @impl
    async def impl1(cls, update: UpdateNode) -> int:
        if update.update_id >= 10000:
            return update.update_id
        raise ComposeError("Update id < 10000")


@dataclasses.dataclass(slots=True, frozen=True)
class DataMorphNode(Polymorphic, DataNode):
    update_id: int

    @impl
    async def impl1(cls, update: UpdateNode) -> typing.Self:
        if update.update_id >= 10000:
            return cls(update.update_id)
        raise ComposeError("Update id < 10000")


class StringNode(Node):
    @classmethod
    async def compose(cls, update: UpdateNode) -> str:
        return str(update.update_id)


@pytest.mark.asyncio()
async def test_scalar_morph(api_instance, message_update):
    result = await compose_nodes(
        {"scalar_morph": ScalarMorphNode},  # type: ignore
        Context(),
        {API: api_instance, Update: message_update},  # type: ignore
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert result.value.values == {"scalar_morph": 12345}


@pytest.mark.asyncio()
async def test_data_morph(api_instance, message_update):
    result = await compose_nodes(
        {"data_morph": DataMorphNode}, Context(), {API: api_instance, Update: message_update}
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert result.value.values == {"data_morph": DataMorphNode(12345)}


@pytest.mark.asyncio()
async def test_node(api_instance, message_update):
    result = await compose_nodes({"string": StringNode}, Context(), {API: api_instance, Update: message_update})
    assert result
    assert isinstance(result.value, NodeCollection)
    assert result.value.values == {"string": "12345"}


@pytest.mark.asyncio()
async def test_message_node(api_instance, message_update):
    result = await compose_nodes(
        {"message": MessageNode},  # type: ignore
        Context(),
        {API: api_instance, Update: message_update},
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert "message" in result.value.values and isinstance(result.value.values["message"], MessageCute)


@pytest.mark.asyncio()
async def test_callback_query_node(api_instance, callback_query_update):
    result = await compose_nodes(
        {"callback_query": CallbackQueryNode},  # type: ignore
        Context(),
        {API: api_instance, Update: callback_query_update},
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert "callback_query" in result.value.values and isinstance(
        result.value.values["callback_query"], CallbackQueryCute
    )


@pytest.mark.asyncio()
@with_mocked_api(GET_ME_RAW_RESPONSE)
async def test_me_node(api: API):
    result = await compose_nodes({"me": Me}, Context(), {API: api})  # type: ignore
    assert result
    assert isinstance(result.value, NodeCollection)
    assert "me" in result.value.values and isinstance(result.value.values["me"], User)
    assert result.value.values["me"].id == 55732494


@pytest.mark.asyncio()
async def test_event_node_with_dict(api_instance, message_update):
    result = await compose_nodes(
        {"event": EventNode[dict[str, typing.Any]]},  # type: ignore
        Context(),
        {API: api_instance, Update: message_update, Context: Context()},
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert "event" in result.value.values and isinstance(result.value.values["event"], dict)
    assert result.value.values["event"] == message_update.message.unwrap().to_full_dict()


@pytest.mark.asyncio()
async def test_event_node_with_message_object(api_instance, message_update):
    result = await compose_nodes(
        {"event": EventNode[Message]},  # type: ignore
        Context(),
        {API: api_instance, Update: message_update, Context: Context()},
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert "event" in result.value.values and isinstance(result.value.values["event"], Message)
    assert result.value.values["event"] == message_update.message.unwrap()


@pytest.mark.asyncio()
async def test_rule_chain(api_instance, message_update):
    result = await compose_nodes(
        {"rule_chain": PrettyRuleChain},  # type: ignore
        Context(),
        {API: api_instance, Update: message_update},
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert (
        "rule_chain" in result.value.values
        and result.value.values["rule_chain"].__class__.__name__ == "PrettyRuleChain"
    )
    assert dataclasses.is_dataclass(result.value.values["rule_chain"]) and dataclasses.asdict(
        result.value.values["rule_chain"]  # type: ignore
    ) == {  # type: ignore
        "framework": "Telegrinder",
        "logical_lang": "laurelang",
        "smile": "^_^",
    }


@pytest.mark.asyncio()
async def test_node_generator(api_instance, message_update):
    MyNode = generate_node(  # noqa: N806
        (Text,),  # type: ignore
        func=lambda text: text
        if text == "Hello, Telegrinder! btw, laurelang - nice pure logical programming launguage ^_^"
        else False,
    )
    result = await compose_nodes(
        {"my_node": MyNode},
        Context(),
        {API: api_instance, Update: message_update},
    )
    assert result
    assert isinstance(result.value, NodeCollection)
    assert "my_node" in result.value.values and isinstance(result.value.values["my_node"], str)
