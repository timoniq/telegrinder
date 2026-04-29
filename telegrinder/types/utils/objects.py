import typing

from kungfu.library.monad.option import Some

from telegrinder.types.default_params import DEFAULT_PARAMETERS, DefaultParameters

if typing.TYPE_CHECKING:
    type DefaultFactory = typing.Callable[[], typing.Any]

    def _f[**P](_: typing.Callable[P, typing.Any], /) -> typing.Callable[P, DefaultFactory]: ...

    default_parameter_for_field = _f(DefaultParameters().get)  # type: ignore
    default_parameter_as_option_for_field = _f(DefaultParameters().get)  # type: ignore
else:
    _NODEFAULT: typing.Final[typing.Any] = object()

    def _get_proxy_default_parameter(parameter_name: str, /) -> typing.Any:
        return DEFAULT_PARAMETERS[parameter_name]

    def default_parameter_for_field(
        k: str,
        default: typing.Any = _NODEFAULT,
    ) -> DefaultFactory:
        proxy_default_parameter = _get_proxy_default_parameter(k)
        return lambda: (
            proxy_default_parameter.get_or_error()
            if default is _NODEFAULT
            else proxy_default_parameter.get_or_default(default)
        )

    def default_parameter_as_option_for_field(
        k: str,
        default: typing.Any = _NODEFAULT,
    ) -> DefaultFactory:
        proxy_default_parameter = _get_proxy_default_parameter(k)
        return lambda: (
            proxy_default_parameter.get_or_nothing()
            if default is _NODEFAULT
            else Some(proxy_default_parameter.get_or_default(default))
        )


__all__ = ("default_parameter_as_option_for_field", "default_parameter_for_field")
