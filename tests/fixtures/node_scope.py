import pytest
from nodnod.interface.inject import inject_internals
from nodnod.scope import Scope

from telegrinder.api.api import API
from telegrinder.types.objects import Update


def make_node_scope(api: API, update: Update) -> Scope:
    scope = Scope()
    inject_internals(scope, {API: api, Update: update})
    return scope


@pytest.fixture()
def node_scope_factory(api_instance: API):
    def factory(update: Update) -> Scope:
        return make_node_scope(api_instance, update)

    return factory


@pytest.fixture()
def message_node_scope(api_instance: API, message_update: Update) -> Scope:
    return make_node_scope(api_instance, message_update)


@pytest.fixture()
def callback_query_node_scope(api_instance: API, callback_query_update: Update) -> Scope:
    return make_node_scope(api_instance, callback_query_update)
