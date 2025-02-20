import pathlib

import pytest

from .test_utils import MockedHttpClient

RESPONSE_KITTEN_BYTES = pathlib.Path("examples/assets/kitten.jpg").read_bytes()
RESPONSE_JSON = {
    "ok": True,
    "response": {
        "count": 1,
        "items": [
            {
                "item": "Box",
                "price": 5295.0,
                "quantity": 1,
                "description": "Box of things",
                "image": b"XXXXXXXXXXXXXXXXXX",
                "id": 9327156890021313285781,
                "created": "11.11.2009",
                "updated": "09.01.2019",
                "deleted": "30.12.2023",
                "from": "USA",
            }
        ],
    },
}


@pytest.mark.asyncio()
async def test_http_request_text():
    client = MockedHttpClient("response")
    response = await client.request_text("https://site.com")
    await client.close()

    assert isinstance(response, str)
    assert response.islower()
    assert response == "response"


@pytest.mark.asyncio()
async def test_http_request_content():
    client = MockedHttpClient(RESPONSE_KITTEN_BYTES)
    response = await client.request_content("https://kitten.com", data={"image": "jpg"})
    await client.close()

    assert isinstance(response, bytes)
    assert response == RESPONSE_KITTEN_BYTES


@pytest.mark.asyncio()
async def test_http_request_json():
    client = MockedHttpClient(RESPONSE_JSON)
    response = await client.request_json("https://megashop.net", data={"item": "Box"})
    await client.close()

    assert isinstance(response, dict)
    assert response == RESPONSE_JSON
    assert response["response"]["items"][0]["item"] == "Box"
    assert response["response"]["items"][0]["price"] == 5295.0


@pytest.mark.asyncio()
async def test_http_request_bytes():
    client = MockedHttpClient(b"response")
    response = await client.request_bytes("https://kitten.com", data={"image": "jpg"})
    await client.close()

    assert isinstance(response, bytes)
    assert response == b"response"
