import pytest
from fntypes.error import UnwrapError

from telegrinder.api.api import API
from telegrinder.api.error import APIError
from telegrinder.api.response import APIResponse
from telegrinder.msgspec_utils import decoder
from telegrinder.types.objects import User
from tests.test_utils import with_mocked_api

API_ERROR_RESPONSE = {
  "ok": False,
  "error_code": 404,
  "description": "Not Found"
}

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
GET_ME_USER_DICT = decoder.decode(GET_ME_RAW_RESPONSE, type=dict)
GET_ME_API_RESPONSE = decoder.decode(GET_ME_RAW_RESPONSE, type=APIResponse).to_result()
GET_ME_USER_MODEL = decoder.decode(GET_ME_API_RESPONSE.unwrap(), type=User)


@pytest.mark.asyncio()
@with_mocked_api(GET_ME_RAW_RESPONSE)
async def test_get_me_raw(api: API):
    raw_me = await api.request_raw("getMe")

    assert raw_me
    assert raw_me == GET_ME_API_RESPONSE
    assert raw_me.unwrap() == GET_ME_API_RESPONSE.unwrap()


@pytest.mark.asyncio()
@with_mocked_api(GET_ME_RAW_RESPONSE)
async def test_get_me_method(api: API):
    me = await api.get_me()

    assert me
    assert me.unwrap() == GET_ME_USER_MODEL
    assert me.unwrap().id == 55732494
    assert me.unwrap().first_name == "Cute"
    assert me.unwrap().is_bot == True


@pytest.mark.asyncio()
@with_mocked_api(GET_ME_USER_DICT)
async def test_api_request_method(api: API):
    response = await api.request("getMe")

    assert response
    assert response.unwrap() == GET_ME_USER_DICT["result"]
    assert isinstance(response.value, dict)
    assert response.value["id"] == GET_ME_USER_DICT["result"]["id"]
    assert response.value["first_name"] == GET_ME_USER_DICT["result"]["first_name"]
    assert response.value["is_bot"] == GET_ME_USER_DICT["result"]["is_bot"]


@pytest.mark.asyncio()
@with_mocked_api(API_ERROR_RESPONSE)
async def test_api_error(api: API):
    response = await api.request("someMethod")

    assert not response
    assert isinstance(response.error, APIError)
    assert response.error.code == 404
    assert response.error.error == "Not Found"
    with pytest.raises(UnwrapError, match="Not Found"):
        response.unwrap()
