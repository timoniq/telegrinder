from __future__ import annotations

import abc
import dataclasses
import types
import typing

from telegrinder.tools.keyboard.buttons import BaseButton
from telegrinder.tools.keyboard.keyboard import AnyMarkup, DictStrAny, KeyboardModel
from telegrinder.tools.keyboard.static_buttons import BaseStaticButton, StaticButton, StaticInlineButton
from telegrinder.types.objects import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

KEYBOARD_BUTTONS_KEY: typing.Final[str] = "_buttons"
KEYBOARD_BUTTON_CLASS_KEY: typing.Final[str] = "_button_class"
NO_VALUE: typing.Final[object] = object()


def _has_under(name: str, /) -> bool:
    return name.startswith("_")


def _get_buttons(cls_: type[typing.Any], /) -> dict[str, typing.Any]:
    return {k: v for k, v in dict(vars(cls_)).items() if isinstance(v, cls_.get_button_class())}


def make_keyboard[T: BaseStaticButton](
    cls_: type[BaseStaticKeyboard[T]],
    /,
) -> typing.Iterable[typing.Iterable[DictStrAny]]:
    buttons = cls_.get_buttons()
    max_in_row = cls_.max_in_row
    keyboard = [[]]

    for button in buttons.values():
        if button.row is True or len(keyboard[-1]) >= max_in_row:
            keyboard.append([])
        keyboard[-1].append(button.get_data())

    return tuple(tuple(x) for x in keyboard if x)


class StaticKeyboardMeta(type):
    if not typing.TYPE_CHECKING:

        def __getattr__(cls, name, /):
            if not _has_under(name):
                buttons = _get_buttons(cls)
                if name in buttons:
                    return buttons[name]
            return super().__getattribute__(name)

    def __setattr__(cls, name: str, value: typing.Any, /) -> None:
        if not _has_under(name) and name in _get_buttons(cls):
            raise AttributeError(f"Cannot reassing attribute {name!r}.")
        return super().__setattr__(name, value)

    def __delattr__(cls, name: str, /) -> None:
        if not _has_under(name) and name in _get_buttons(cls):
            raise AttributeError(f"Cannot delete attribute {name!r}.")
        return super().__delattr__(name)


class ABCStaticKeyboardMeta(abc.ABCMeta, StaticKeyboardMeta):
    pass


class ABCStaticKeyboard[T: BaseStaticButton](metaclass=ABCStaticKeyboardMeta):
    @abc.abstractmethod
    def dict(self) -> DictStrAny:
        pass

    @abc.abstractmethod
    def get_markup(self) -> AnyMarkup:
        pass

    @classmethod
    def get_button_class(cls) -> type[T]:
        if (button_class := getattr(cls, KEYBOARD_BUTTON_CLASS_KEY, None)) is not None:
            return typing.cast("type[T]", button_class)

        parametrized_base = None
        original_bases = list(types.get_original_bases(cls))

        while original_bases:
            base = original_bases.pop(0)
            orig_base = typing.get_origin(base) or base
            if orig_base is not ABCStaticKeyboard and issubclass(orig_base, ABCStaticKeyboard):
                original_bases.extend(types.get_original_bases(orig_base))
                parametrized_base = base

        if parametrized_base is None:
            raise TypeError(f"{cls.__name__!r} has no ABCStaticKeyboard original base class.")

        args = typing.get_args(parametrized_base)
        if not args:
            raise TypeError(f"{cls.__name__!r} has no parameters in generic.")

        maybe_button_class = typing.get_origin(args[0]) or args[0]
        if not isinstance(maybe_button_class, type):
            maybe_button_class = type(maybe_button_class)

        if not issubclass(maybe_button_class, BaseButton):
            raise TypeError(f"Parameter {maybe_button_class!r} is not subclass of BaseButton.")

        button_class = typing.cast("type[T]", maybe_button_class)
        setattr(cls, KEYBOARD_BUTTON_CLASS_KEY, button_class)
        return button_class

    @classmethod
    def get_buttons(cls) -> dict[str, T]:
        return _get_buttons(cls)


class BaseStaticKeyboard[T: BaseStaticButton](ABCStaticKeyboard[T]):
    max_in_row: int

    def __init_subclass__(cls, *, max_in_row: int = 3) -> None:
        cls.max_in_row = max_in_row
        return super().__init_subclass__()

    @classmethod
    def get_buttons(cls) -> dict[str, T]:
        if (buttons := cls._get_secret_value(KEYBOARD_BUTTONS_KEY)) is not NO_VALUE:
            return buttons
        return cls._set_secret_value(KEYBOARD_BUTTONS_KEY, super().get_buttons())

    @classmethod
    def _set_secret_value[V](cls, key: str, value: V, /) -> V:
        setattr(cls, key, value)
        return value

    @classmethod
    def _get_secret_value(cls, key: str, /) -> typing.Any:
        return getattr(cls, key, NO_VALUE)


class StaticKeyboard(BaseStaticKeyboard[StaticButton]):
    __keyboard__: KeyboardModel

    def __init_subclass__(
        cls,
        *,
        resize_keyboard: bool = True,
        one_time_keyboard: bool = False,
        selective: bool = False,
        is_persistent: bool = False,
        max_in_row: int = 3,
    ) -> None:
        super().__init_subclass__(max_in_row=max_in_row)
        cls.__keyboard__ = KeyboardModel(
            resize_keyboard=resize_keyboard,
            one_time_keyboard=one_time_keyboard,
            selective=selective,
            is_persistent=is_persistent,
            keyboard=make_keyboard(cls),
        )

    @classmethod
    def dict(cls) -> DictStrAny:
        return dataclasses.asdict(cls.__keyboard__)

    @classmethod
    def get_markup(cls) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup.from_dict(cls.dict())

    @classmethod
    def get_keyboard_remove(cls) -> ReplyKeyboardRemove:
        return ReplyKeyboardRemove.from_data(
            remove_keyboard=True,
            selective=cls.__keyboard__.selective,
        )


class StaticInlineKeyboard(BaseStaticKeyboard[StaticInlineButton]):
    __keyboard__: typing.Iterable[typing.Iterable[DictStrAny]]

    def __init_subclass__(cls, *, max_in_row: int = 3) -> None:
        super().__init_subclass__(max_in_row=max_in_row)
        cls.__keyboard__ = make_keyboard(cls)

    @classmethod
    def dict(cls) -> DictStrAny:
        return dict(inline_keyboard=cls.__keyboard__)

    @classmethod
    def get_markup(cls) -> InlineKeyboardMarkup:
        return InlineKeyboardMarkup.from_dict(cls.dict())


__all__ = ("ABCStaticKeyboard", "BaseStaticKeyboard", "StaticInlineKeyboard", "StaticKeyboard")
