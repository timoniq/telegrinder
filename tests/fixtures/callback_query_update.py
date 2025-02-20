import pytest

from telegrinder.types.objects import Update

UPDATE = Update.from_raw(
    b"""
    {
        "update_id":12345,
        "callback_query":{
            "id":"4382bfdwdsb323b2d9",
            "from":{
                "last_name":"Test Lastname",
                "type":"private",
                "id":1111111,
                "is_bot":false,
                "first_name":"Test Firstname",
                "username":"Testusername"
            },
            "chat_instance":"23asinstance23442",
            "data":"Data from button callback",
            "inline_message_id":"1234csdbsk4839",
            "message":{
                "message_id": 23423522,
                "from":{
                    "last_name":"Test Lastname",
                    "type": "private",
                    "id":1111111,
                    "is_bot":false,
                    "first_name":"Test Firstname",
                    "username":"Testusername"
                },
                "chat": {
                    "last_name":"Test Lastname",
                    "type": "private",
                    "id":1111111,
                    "is_bot":false,
                    "first_name":"Test Firstname",
                    "username":"Testusername"
                },
                "date":1234567898,
                "text":"Hello, Telegrinder! btw, laurelang - nice pure logical programming launguage ^_^"
            }
        }
    }
    """
)


@pytest.fixture()
def callback_query_update():
    return UPDATE
