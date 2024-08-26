import pytest

from telegrinder.types.objects import Update

UPDATE = Update.from_bytes(
    b"""
    {
        "update_id": 10000,
        "callback_query": {
            "id": "4382bfdwdsb323b2d9",
            "from":{
                "last_name":"Test Lastname",
                "type": "private",
                "id":1111111,
                "is_bot":false,
                "first_name":"Test Firstname",
                "username":"Testusername"
            },
            "chat_instance": "23asinstance23442",
            "data": "Data from button callback",
            "inline_message_id": "1234csdbsk4839"
        }
    }
    """
)


@pytest.fixture()
def callback_query_update():
    return UPDATE
