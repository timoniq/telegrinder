import hashlib
import hmac
import typing

from telegrinder.api.abc import Token


def verify_webapp_request(secret_token: str, request_headers: dict[str, typing.Any]) -> bool:
    """Verifies update request is from telegram."""

    return request_headers.get("X-Telegram-Bot-Api-Secret-Token") == secret_token


def webapp_validate_request(
    bot_token: Token,
    request_query_params: dict[str, typing.Any],
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
    return data_chk.hexdigest() == request_query_params.get("hash")


__all__ = ("verify_webapp_request", "webapp_validate_request")
