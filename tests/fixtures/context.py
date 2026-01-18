import pytest

from telegrinder.api.api import API
from telegrinder.bot.dispatch.context import Context
from telegrinder.types.objects import Update

from .node_scope import make_node_scope


def make_context(api: API, update: Update) -> Context:
    scope = make_node_scope(api, update)
    ctx = Context()
    ctx.add_roots(api, update, scope)
    return ctx


@pytest.fixture()
def context_factory(api_instance: API):
    def factory(update: Update) -> Context:
        return make_context(api_instance, update)

    return factory


@pytest.fixture()
def message_context(api_instance: API, message_update: Update) -> Context:
    return make_context(api_instance, message_update)


@pytest.fixture()
def callback_query_context(api_instance: API, callback_query_update: Update) -> Context:
    return make_context(api_instance, callback_query_update)
