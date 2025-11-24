from http import HTTPStatus

from kungfu import Error, Ok, Result

from telegrinder.api.api import API
from telegrinder.api.error import InvalidTokenError
from telegrinder.api.token import Token


async def validate_token(token: str, /) -> Result[Token, InvalidTokenError]:
    try:
        token = Token(token)
        api = API(token)

        match await api.get_me():
            case Ok(_):
                return Ok(token)
            case Error(error):
                return Error(
                    InvalidTokenError(
                        "Token seems to be invalid."
                        if error.status_code in (HTTPStatus.UNAUTHORIZED, HTTPStatus.NOT_FOUND)
                        else f"Unknown error {error!r} while validating token, please try again later.",
                    ),
                )
    except InvalidTokenError as error:
        return Error(error)


__all__ = ("validate_token",)
