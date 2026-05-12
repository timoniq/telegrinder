# Обработка ошибок

Ошибки в боте неизбежны: сеть, пользовательский ввод, внешние API, база данных, собственная логика. В telegrinder у dispatch есть встроенный путь для обработки исключений через `event_error`.

## Базовый пример

```python
from telegrinder import Message
from telegrinder.node import Error
from telegrinder.rules import IsUser, Text


@bot.on.message(Text("oops"))
async def oops_handler(message: Message) -> None:
    await message.answer("Oh no")
    raise RuntimeError("Wow")


@bot.on.message(Text("woops"))
def woops_handler() -> None:
    raise ValueError("Wow oopsii!")


@bot.on.event_error(IsUser())
async def error_handler(err: Error[RuntimeError, ValueError], message: Message) -> None:
    await message.answer(f"Что-то пошло не так: {err.exception}")
```

Здесь происходит следующее:

- обычный handler выбрасывает исключение
- dispatch ловит его
- событие маршрутизируется во view `event_error`
- в error handler можно получить ноду `Error[...]`

---

## Нода Error

`Error[...]` это generic node. Её можно ограничить конкретными типами исключений:

```python
err: Error[RuntimeError]
err: Error[ValueError, TypeError]
err: Error[Exception]
```

Если тип исключения не подходит, такая нода не соберётся, и обработчик не будет считаться подходящим.

Это удобно, когда хочется развести обработку:

- бизнес-ошибки отдельно
- ошибки валидации отдельно
- неожиданные ошибки отдельно

---

## Где лучше ловить исключения

Общий практический подход:

- локально обрабатывайте ожидаемые ошибки, если от них зависит конкретный ответ пользователю
- используйте `event_error` для общей страховки и централизованного логирования
- не прячьте молча исключения, если это ломает диагностику

Если ошибка означает “пользователь сделал что-то не так”, часто лучше ответить прямо в обычном handler. Если это системная авария, её удобно пропустить в `event_error`.

---

## Error view у router и dispatch

Важно помнить, что ошибки обрабатываются не где-то “снаружи бота”, а внутри dispatch/router-модели:

- у router есть `event_error`
- у dispatch есть `error_handler`
- при загрузке нескольких dispatch error views тоже объединяются

Из-за этого обработка ошибок остаётся частью той же архитектуры, что и обработка обычных событий.

---

## Что посмотреть в примерах

- [examples/error_catching.py](https://github.com/timoniq/telegrinder/blob/dev/examples/error_catching.py)
- [examples/action.py](https://github.com/timoniq/telegrinder/blob/dev/examples/action.py)

[>> Next: Готовые сценарии](12_out-of-box_scenarios.md)
