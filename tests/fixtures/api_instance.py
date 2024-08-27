import pytest

from telegrinder.api.api import API, Token

from ..test_utils import MockedHttpClient


@pytest.fixture()
def api_instance():
    return API(Token("123:ABCdef"), http=MockedHttpClient())
