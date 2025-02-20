import pytest

from telegrinder.types.objects import Update

UPDATE = Update.from_raw(
    b"""
    {
        "update_id": 12345,
        "message": {
            "message_id": 23423522,
            "from": {
                "id": 123,
                "is_bot": false,
                "first_name": "John",
                "last_name": "Doe",
                "username": "Johndoe333",
                "language_code": "en"
            },
            "chat": {
                "id": 123,
                "first_name": "John",
                "last_name": "Doe",
                "is_bot": false,
                "username": "Johndoe333",
                "type": "private"
            },
            "date": 1234567898,
            "text": "Hello, Telegrinder! btw, laurelang - nice pure logical programming launguage ^_^"
        }
    }
    """
)


@pytest.fixture()
def message_update():
    return UPDATE
