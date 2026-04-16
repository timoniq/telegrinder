import msgspec
from kungfu.library.monad.result import Error, Ok

from telegrinder.api.error import APIError
from telegrinder.types.utils import full_result


def test_full_result_is_lazy_until_unwrap(mocker):
    decode = mocker.patch("telegrinder.types.utils.methods.decode_full_result", return_value=123)

    result = full_result(Ok(msgspec.Raw(b"123")), int)

    decode.assert_not_called()
    assert result.unwrap() == 123
    decode.assert_called_once_with(msgspec.Raw(b"123"), int)


def test_full_result_is_lazy_for_map(mocker):
    decode = mocker.patch("telegrinder.types.utils.methods.decode_full_result", return_value=10)

    result = full_result(Ok(msgspec.Raw(b"10")), int)
    mapped = result.map(lambda value: value + 5)

    decode.assert_called_once_with(msgspec.Raw(b"10"), int)
    assert mapped.unwrap() == 15


def test_full_result_is_lazy_for_pattern_matching(mocker):
    decode = mocker.patch("telegrinder.types.utils.methods.decode_full_result", return_value=42)

    result = full_result(Ok(msgspec.Raw(b"42")), int)

    decode.assert_not_called()

    match result:
        case Ok(value):
            assert value == 42
        case _:
            assert False, "Expected Ok result"

    decode.assert_called_once_with(msgspec.Raw(b"42"), int)


def test_full_result_keeps_error_unchanged(mocker):
    decode = mocker.patch("telegrinder.types.utils.methods.decode_full_result")
    error = APIError(code=400, error="bad request", data={})

    result = full_result(Error(error), int)

    assert result is not None
    assert isinstance(result, Error)
    assert result.error == error
    decode.assert_not_called()
