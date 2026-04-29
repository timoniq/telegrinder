import hashlib
import hmac
import typing
from contextlib import suppress
from urllib.parse import parse_qsl

SECRET_TOKEN_KEY: typing.Final = "X-Telegram-Bot-Api-Secret-Token"


def verify_secret_token(
    secret_token: str,
    request_headers: typing.Mapping[str, typing.Any],
) -> bool:
    """Verifies update request is from telegram."""
    return request_headers.get(SECRET_TOKEN_KEY) == secret_token


def webapp_validate_raw(bot_token: str, raw_data: str) -> bool:
    """Verifies raw authentity of webapp request by counting hash of its parameters."""

    with suppress(ValueError):
        return webapp_validate_request(
            bot_token,
            dict(parse_qsl(raw_data, strict_parsing=True)),
        )

    return False  # pragma: no cover


def webapp_validate_request(
    bot_token: str,
    request_query_params: typing.Mapping[str, typing.Any],
) -> bool:
    """Verifies authentity of webapp request by counting hash of its parameters."""
    items = sorted(request_query_params.items(), key=lambda kv: kv[0])
    data_check_string = "\n".join(f"{k}={param}" for k, param in items if k != "hash")
    secret = hmac.new(
        "WebAppData".encode(),
        bot_token.encode(),
        hashlib.sha256,
    ).digest()
    data_chk = hmac.new(secret, data_check_string.encode(), hashlib.sha256)

    if (hash_ := request_query_params.get("hash")) is None:
        return False
    return hmac.compare_digest(data_chk.hexdigest(), hash_)


__all__ = ("verify_secret_token", "webapp_validate_raw", "webapp_validate_request")
