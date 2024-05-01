# Keyboard set

It's easy to create a keyboard set, keyboards can be loaded from YAML config.

[Click for example](https://github.com/timoniq/telegrinder/blob/main/examples/kb_set.py)

Snippet from example:

```python
class KeyboardSet(KeyboardSetYAML):
    __config__ = "assets/kb_set_config.yaml"

    KEYBOARD_MENU: Keyboard
    KEYBOARD_YES_NO: Keyboard
    KEYBOARD_ITEMS: InlineKeyboard
```

Specify which type of Keyboard generator you will use, it should correspond to ABCMarkup interface.

All the contents of the keyboard should be stored in file with path declared in `__config__`, by default it is `keyboards.yaml`.

Keyboards are named with lowercase names of fields without `KEYBOARD_`/`KB_` start.

For example, field name for `KEYBOARD_MENU` is `menu`.

Each keyboard in yaml format should obtain `buttons` field. `buttons` should be a list of buttons with fields declared in telegram docs (`text` field is required).

In addition special fields like `one_time_keyboard` can be declared.

Snippet from [`assets/kb_set_config.yaml`](https://github.com/timoniq/telegrinder/blob/main/examples/assets/kb_set_config.yaml):

```yaml
menu:
  buttons:
    - text: "Choose"
    - text: "Edit"
yes_no:
  one_time_keyboard: on
  buttons:
    - text: "Yes"
    -
    - text: "No"
```

An empty element in `buttons` list (`- `) will move buttons after it to the next row.
