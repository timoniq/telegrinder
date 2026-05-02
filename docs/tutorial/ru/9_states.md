# Стейты (состояния пользователя): waiters, длинные стейты

Это один из самых важных разделов для реального бота.

Почти любой бот рано или поздно сталкивается с такими ситуациями:

- пользователь начал сценарий, но не закончил его за одно сообщение
- бот ждёт следующий ответ
- у пользователя есть "режим", в котором он сейчас находится
- интерфейс зависит от предыдущих действий

Именно здесь появляются состояния.

В telegrinder для этого есть несколько уровней инструментов:

- `State(...)` + storage для долгоживущих состояний
- waiter machine для коротких ожиданий
- `choice` и `checkbox` для готовых интерактивных шагов
- `state_mutator` для более сложной и типизированной state-модели

Если коротко:

- storage это "у пользователя сейчас такое состояние"
- waiter это "я жду следующий шаг"
- state mutator это "я хочу описывать переходы между состояниями как нормальную модель"

## Самый простой старт: storage

Если вы только начинаете, проще всего стартовать с `MemoryStateStorage`.

```python
import enum

from telegrinder import MemoryStateStorage, Message, StateData
from telegrinder.rules import StateMeta, Text

states = MemoryStateStorage()


class StateEnum(enum.StrEnum):
    CURSED = "cursed"
    BLESSED = "blessed"


@bot.on.message(
    Text("/curse"),
    # Команду /curse можно вызвать, если пользователь blessed
    # или если у него вообще ещё нет состояния.
    states.State(StateEnum.BLESSED) | states.State(StateMeta.NO_STATE),
)
async def curse_handler(message: Message) -> None:
    await states.set(message.from_user.id, StateEnum.CURSED, {})
    await message.answer("Теперь ты cursed.")


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

### Что здесь важно

Storage хранит `StateData`, в котором есть:

- `key` — имя состояния
- `payload` — дополнительные данные

Проверять состояние можно через rule:

```python
states.State(StateEnum.CURSED)
states.State(StateMeta.NO_STATE)
states.State(StateMeta.ANY)
```

Это уже закрывает очень много прикладных задач.

Например:

- пользователь в режиме оформления заказа
- пользователь проходит onboarding
- пользователь уже авторизован
- пользователь сейчас редактирует профиль

> [!TIP]
> Если вам нужно просто "запомнить режим пользователя", не начинайте сразу с `state_mutator`. Обычный storage проще и часто полностью достаточен.

---

## Чтение, запись и удаление состояния

Самая частая тройка операций:

- `set(...)`
- `get(...)`
- `delete(...)`

```python
await states.set(user_id, StateEnum.BLESSED, {"source": "admin"})
state = await states.get(user_id)
await states.delete(user_id)
```

`MemoryStateStorage` хорош для:

- локальной разработки
- тестов
- маленьких ботов

Но он не переживает рестарт процесса.

Если состояние должно жить дольше, обычно делают свою реализацию `ABCStateStorage` поверх Redis, базы данных или другого внешнего хранилища.

> [!TIP]
> Если после перезапуска бота состояние "теряется" и это ломает опыт использования, значит пора уходить с `MemoryStateStorage` на внешнее хранилище.

---

## Когда storage удобнее всего

Storage очень хорош, когда состояние похоже на "флажок" или "режим":

- пользователь сейчас в wizard-е
- пользователь заблокирован
- пользователь выбрал язык
- пользователь находится на шаге 3 из 5

Если состояние нужно просто проверить правилом перед хендлером, storage обычно самый прямой и понятный выбор.

---

## Waiters: когда бот ждёт следующий шаг

Не всегда хочется хранить состояние долго.

Иногда бот делает что-то гораздо проще:

- задал вопрос
- ждёт один следующий ответ
- продолжает сценарий

Вот для этого нужна waiter machine.

Она уже встроена в dispatch и views, поэтому отдельно поднимать её обычно не нужно.

Практически это даёт возможность:

- дождаться следующего сообщения
- дождаться нажатия inline-кнопки
- ограничить время ожидания
- применить фильтры к тому, что считается "подходящим" ответом

Это особенно полезно для коротких воронок и интерактивных шагов.

---

## Готовые сценарии `Choice` и `Checkbox`

Очень часто руками собирать waiter вообще не нужно.

### `Choice`

Это хороший вариант, когда в конце должен быть выбран ровно один вариант.

```python
@bot.on.message(Text("/choice"))
async def action(message: Message) -> None:
    chosen, message_id = await (
        bot.dispatch.choice(message.chat.id, message="Choose something", max_in_row=1)
        # Первый текст — обычный, второй — вид выбранного варианта.
        .add_option("apple", "Apple 🔴", "Apple 🟢")
        .add_option("banana", "Banana 🔴", "Banana 🟢", is_picked=True)
        .add_option("pear", "Pear 🔴", "Pear 🟢")
        .wait(message.api)
    )

    await message.edit(
        text=f"You chose: {chosen}",
        message_id=message_id,
    )
```

### `Checkbox`

Это вариант, когда можно выбрать несколько элементов.

```python
@bot.on.message(Text("/checkbox"))
async def action(message: Message) -> None:
    picked, message_id = await (
        bot.dispatch.checkbox(
            message.chat_id,
            message="Check your checkbox",
            cancel_text="Cancel",
            max_in_row=2,
        )
        .add_option("apple", "Apple", "Apple 🍏")
        .add_option("banana", "Banana", "Banana 🍌", is_picked=True)
        .add_option("pear", "Pear", "Pear 🍐")
        .wait(message.api)
    )

    await message.edit(
        text="You picked: {}".format(", ".join(key for key, value in picked.items() if value)),
        chat_id=message.chat.id,
        message_id=message_id,
    )
```

Это очень дружелюбный путь для новичка:

- не нужно руками проектировать callback flow
- не нужно вручную собирать keyboard state
- не нужно самостоятельно держать короткое состояние шага

---

## Где тут `state_mutator`

Вот здесь начинается другой уровень.

Если storage отвечает на вопрос:

"какое у пользователя состояние сейчас?"

то `state_mutator` отвечает на вопрос:

"как вообще устроена модель состояний и переходов между ними?"

Это полезно, когда у вас не просто "одна строка в storage", а действительно сценарий с переходами.

Примеры:

- плеер: `Stopped -> Playing -> Paused`
- персонаж в игре: `Alive -> Dead -> Alive`
- заказ: `Draft -> WaitingPayment -> Paid -> Shipped`

В таких случаях `state_mutator` делает модель гораздо приятнее и безопаснее.

---

## Первая модель на `state_mutator`

Начнём с дружелюбного примера "жив / мёртв".

```python
import dataclasses
import datetime

from telegrinder.tools.state_mutator import State, StateMutator, mutation


@dataclasses.dataclass
class AliveState(State):
    __description__ = "живой"

    # Можно хранить полезные данные прямо в состоянии.
    since: datetime.datetime = dataclasses.field(default_factory=datetime.datetime.now)

    @mutation
    def die(self, reason: str) -> "DeadState":
        # Переход Alive -> Dead
        return DeadState(reason)


@dataclasses.dataclass
class DeadState(State):
    reason: str

    @mutation
    def resurrect(self) -> "AliveState":
        # Переход Dead -> Alive
        return AliveState()

    @property
    def __description__(self) -> str:
        return f"мёртв, причина: {self.reason}"
```

Здесь уже видно главное:

- состояние описывается классом
- переходы описываются методами с `@mutation`
- возвращаемый тип показывает, в какое состояние идёт переход

То есть код начинает читаться почти как предметная модель.

---

## Использование `StateMutator` в хендлерах

Вот как это подключается в боте:

```python
@bot.on.message(Text("/die"))
async def die_handler(alive: AliveState) -> str:
    # Если обработчик вызвался, значит текущее состояние уже AliveState.
    new_state = await alive.die("sadness")
    return f"Теперь ты {new_state.__description__}"


@bot.on.message(Text("/resurrect"))
async def resurrect_handler(dead: DeadState) -> str:
    await dead.resurrect()
    return "Ты воскрес"


@bot.on.message()
async def in_state_handler(state: AliveState | DeadState) -> str:
    # Можно принять union и реагировать на несколько допустимых состояний.
    return f"Сейчас ты {state.__description__}"
```

Что тут особенно приятно:

- если в хендлере принимается `alive: AliveState`, он сработает только когда пользователь действительно в этом состоянии
- переходы вызываются как методы объекта состояния
- код получается очень близким к языку предметной области

> [!TIP]
> Если вы начинаете писать много `if current_state == "...": ... elif current_state == "...": ...`, это хороший сигнал посмотреть в сторону `state_mutator`.

---

## Начальное состояние и "внешние" мутации

Мутация может быть не только методом класса.

```python
from telegrinder.tools.state_mutator import mutation


be_born = mutation(AliveState)


@mutation
def login_as_ghost(silently: bool = False):
    if not silently:
        print("Ghost just logged in ~*_*~")
    return DeadState(reason="~*being a ghost*~")
```

Это полезно, когда переход:

- не принадлежит конкретному состоянию
- является точкой входа в сценарий
- должен запускаться "снаружи"

Использование:

```python
@bot.on.message(Text("/be_born"))
async def be_born_handler(mutator: StateMutator) -> str:
    await be_born(mutator)
    return "Ты родился"


@bot.on.message(Text("Gh0$T_рa$$w0rd"))
async def ghost_handler(mutator: StateMutator) -> str:
    await login_as_ghost(mutator, silently=True)
    return "Теперь ты призрак"
```

Здесь `StateMutator` выступает как объект, который умеет применить переход к текущему пользователю.

---

## Более практичный пример: мини-плеер

Теперь посмотрим на сценарий, который больше похож на реальную модель.

```python
import datetime
from dataclasses import dataclass

from telegrinder.tools.state_mutator import State, mutation


@dataclass
class Stopped(State):
    @mutation
    def play(self, song: str, offset: datetime.timedelta = datetime.timedelta(0)) -> "Playing":
        return Playing(song, offset, datetime.datetime.now())


@dataclass
class Playing(State):
    song: str
    offset: datetime.timedelta
    started_at: datetime.datetime

    @mutation
    def stop(self) -> "Stopped":
        return Stopped()

    @mutation
    def pause(self) -> "Paused":
        offset = datetime.datetime.now() - self.started_at
        return Paused(song=self.song, offset=offset + self.offset, stopped_at=datetime.datetime.now())


@dataclass
class Paused(State):
    song: str
    offset: datetime.timedelta
    stopped_at: datetime.datetime

    @mutation
    def stop(self) -> "Stopped":
        return Stopped()

    @mutation
    def play(self) -> "Playing":
        return Playing(self.song, self.offset, datetime.datetime.now())
```

А теперь хендлеры:

```python
@bot.on.message(Command("play", Argument("song_name", optional=True)))
async def play_song_handler(state: Stopped | Paused | Playing, song_name: str | None = None) -> str:
    match state:
        case Stopped():
            if song_name is None:
                return "Нужно указать песню"

            await state.play(song_name)
            return f"Запустил {song_name}"

        case Paused():
            await state.play()
            return f"Продолжаю {state.song}"

        case Playing():
            return "Уже играет"
```

Почему это хорошо:

- переходы описаны прямо на состояниях
- логика становится очень читаемой
- меньше строковых сравнений
- типы начинают реально помогать

Для сложных ботов это намного приятнее, чем хранить вручную строки вроде `"playing"` и `"paused"` плюс отдельно всё распутывать.

---

## Когда `state_mutator` стоит использовать

Он особенно полезен, если:

- состояний несколько и у них есть явные переходы
- в состоянии нужно хранить данные
- вы хотите, чтобы код читалcя как модель процесса
- обычный storage начинает превращаться в сетку `if/elif`

Если же у вас просто один режим `"waiting_for_name"`, `"waiting_for_email"` и всё, storage может быть проще.

---

## Как выбирать инструмент

Очень практическое правило:

- если нужен просто флаг или режим пользователя, берите storage
- если бот ждёт один ближайший ответ, берите waiter
- если нужен быстрый UX через inline-кнопки, берите `choice` или `checkbox`
- если у вас настоящая машина состояний с переходами, смотрите на `state_mutator`

Не обязательно использовать всё сразу.

Нормально начать с storage и прийти к `state_mutator` только тогда, когда простой подход реально перестал тянуть.

---

## Что запомнить

- states в telegrinder бывают на нескольких уровнях абстракции
- `MemoryStateStorage` это самый простой вход в тему
- waiter machine полезна для коротких интерактивных шагов
- `choice` и `checkbox` закрывают много UX-задач почти без ручной работы
- `state_mutator` хорош там, где состояние это уже не просто строка, а полноценная модель переходов

[>> Next: Медиа](10_media.md)
