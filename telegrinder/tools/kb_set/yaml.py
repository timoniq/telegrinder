from .base import KeyboardSetBase, KeyboardSetError
from telegrinder.tools.keyboard import Keyboard, InlineKeyboard
import typing
import re
import os
import yaml


class KeyboardSetYAML(KeyboardSetBase):
    __config__: str

    @classmethod
    def load(cls) -> None:
        config_path = getattr(cls, "__config__", "keyboards.yaml")
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file for {cls.__name__} is undefined")

        config = yaml.load(open(config_path, "r"), yaml.Loader)
        for name, hint in typing.get_type_hints(cls).items():
            g = re.match(r"(?:kb_|keyboard_)(.+)", name.lower())
            if not g:
                continue

            short_name = g.group(1)
            if short_name not in config:
                raise KeyboardSetError(
                    f"Keyboard {short_name!r} is undefined in config"
                )

            kb_config = config[short_name]

            if (
                not isinstance(kb_config, dict)
                or "buttons" not in kb_config
                or not isinstance(kb_config["buttons"], list)
            ):
                raise KeyboardSetError(
                    "Keyboard should be dict with field buttons which must be a list, "
                    "check documentation"
                )

            buttons = kb_config.pop("buttons")
            new_keyboard: typing.Union[Keyboard, InlineKeyboard] = hint(**kb_config)

            for button in buttons:
                if not button:
                    new_keyboard.row()
                    continue
                if "text" not in button:
                    raise KeyboardSetError("text is required")
                new_keyboard.add(new_keyboard.BUTTON(**button))

            setattr(cls, name, new_keyboard)
