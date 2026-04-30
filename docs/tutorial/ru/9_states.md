# Стейты (состояния пользователя): waiters, длинные стейты

Когда бот начинает вести диалог в несколько шагов, почти сразу появляется состояние:

- пользователь что-то выбрал
- бот ждёт следующий ответ
- дальнейшая логика зависит от предыдущего шага

В telegrinder для этого есть два основных инструмента:

- state storage и правила `State(...)` для долгоживущих состояний
- waiter machine для коротких интерактивных ожиданий

## Долгие состояния через storage

Самый простой стартовый вариант это `MemoryStateStorage`.

```python
import enum

from telegrinder import MemoryStateStorage, Message
from telegrinder.rules import StateMeta, Text

states = MemoryStateStorage()


class StateEnum(enum.StrEnum):
    CURSED = "cursed"
    BLESSED = "blessed"


@bot.on.message(
    Text("/curse"),
    states.State(StateEnum.BLESSED) | states.State(StateMeta.NO_STATE),
)
async def curse_handler(message: Message) -> None:
    await states.set(message.from_user.id, StateEnum.CURSED, {})
    await message.answer("Теперь ты cursed.")
```

Storage хранит `StateData`, где есть:

- `key` — текущее состояние
- `payload` — дополнительные данные состояния

Проверять состояние можно через rule:

```python
states.State(StateEnum.CURSED)
states.State(StateMeta.NO_STATE)
states.State(StateMeta.ANY)
```

---

## Чтение и изменение состояния

```python
@bot.on.message(Text("/bless"), states.State(StateMeta.NO_STATE))
async def bless_handler(message: Message) -> None:
    await states.set(message.from_user.id, StateEnum.BLESSED, {})
    await message.answer("Теперь ты blessed.")


@bot.on.message()
async def any_message_handler(message: Message) -> None:
    state = await states.get(message.from_user.id)
    vibe = state.unwrap_or(StateData("normal", {})).key
    await message.answer(f"Сейчас ты {vibe}.")
```

Состояние можно:

- установить через `set(...)`
- прочитать через `get(...)`
- удалить через `delete(...)`

`MemoryStateStorage` хорош для старта и тестов. Для production обычно делают собственную реализацию `ABCStateStorage` поверх Redis, базы данных или другого внешнего хранилища.

---

## Короткие состояния через waiters

Не всегда нужно хранить состояние долго. Иногда бот просто ждёт один следующий апдейт: ответ на вопрос, нажатие кнопки, подтверждение действия.

Для таких сценариев в telegrinder есть waiter machine. Она уже встроена в dispatch и views.

Практический результат такой:

- можно дождаться следующего сообщения пользователя
- можно дождаться callback query
- можно задать фильтры, release-условия и время жизни

Часть высокоуровневых сценариев на этом и построена.

---

## Готовые сценарии Choice и Checkbox

Если нужен быстрый интерактивный выбор, обычно не надо вручную собирать waiter.

### Choice

```python
@bot.on.message(Text("/choice"))
async def action(message: Message) -> None:
    chosen, message_id = await (
        bot.dispatch.choice(message.chat.id, message="Choose something", max_in_row=1)
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .wait(message.api)
    )
    await message.edit(text=f"You chose: {chosen}", message_id=message_id)
```

### Checkbox

```python
@bot.on.message(Text("/checkbox"))
async def action(message: Message) -> None:
    picked, message_id = await (
        bot.dispatch.checkbox(message.chat_id, message="Check your checkbox", cancel_text="Cancel", max_in_row=2)
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .wait(message.api)
    )
    await message.edit(text=str(picked), chat_id=message.chat.id, message_id=message_id)
```

Эти сценарии очень полезны, когда нужно сделать быстрый UX без ручного управления callback state.

---

## Что выбрать

Обычно правило простое:

- если состояние живёт дольше одного события или переживает рестарт, используйте storage
- если нужно короткое интерактивное ожидание внутри диалога, используйте waiter
- если нужен типовой выбор из кнопок, начните с `choice` или `checkbox`

---

## Что посмотреть в примерах

- [examples/long_states.py](https://github.com/timoniq/telegrinder/blob/dev/examples/long_states.py)
- [examples/choice.py](https://github.com/timoniq/telegrinder/blob/dev/examples/choice.py)
- [examples/checkbox.py](https://github.com/timoniq/telegrinder/blob/dev/examples/checkbox.py)
- [examples/state_mutator.py](https://github.com/timoniq/telegrinder/blob/dev/examples/state_mutator.py)
- [examples/state_mutator_player.py](https://github.com/timoniq/telegrinder/blob/dev/examples/state_mutator_player.py)

[>> Next: Медиа](10_media.md)
