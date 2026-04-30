# Готовые сценарии

После базовых building blocks обычно хочется не просто писать обработчики, а собирать из готовых частей повторяющиеся сценарии. В telegrinder таких сценариев уже достаточно много.

Эта статья не перечисляет весь API, а показывает, какие куски стоит помнить в первую очередь.

## Меню и выбор

Если нужно быстро построить меню:

- используйте статические `Keyboard` и `InlineKeyboard`
- выносите их в отдельные модули
- для выбора одного значения используйте `choice`
- для множественного выбора используйте `checkbox`

Это закрывает большую часть UX-задач для обычного бота без ручной реализации callback state machine.

---

## Разделение проекта

Если бот разрастается:

- делите код на несколько `Dispatch`
- группируйте views через `Router`
- собирайте приложение через `load_many` или `load_from_dir`

Это один из самых полезных сценариев “из коробки”, потому что он влияет на поддержку проекта сильнее, чем любой отдельный helper.

---

## Диалоги и состояния

Для диалогов у вас есть несколько уровней абстракции:

- `State` + storage для долгих состояний
- waiter machine для коротких ожиданий
- `choice` и `checkbox` как готовые интерактивные сценарии
- `state_mutator`, если нужен более управляемый сценарий со сложной логикой состояний

Если не уверены, с чего начать, начинайте с самого простого:

- storage для “текущего режима пользователя”
- waiter для “жду ответ на один вопрос”

---

## Payload-модели

Для inline-меню и действий почти всегда выгодно использовать не строковые конкатенации, а payload-модели:

- они типизированы
- их проще расширять
- их проще проверять через `PayloadModelRule`

Особенно это помогает в магазинах, админках, пагинации и многошаговых меню.

---

## Медиа и вложения

Из коробки удобно работают:

- reply shortcuts у cute types
- attachment nodes
- `File[...]`
- `MediaGroup`

Поэтому большую часть медиа-логики можно писать на уровне “что я хочу получить”, а не “как именно это разобрать из сырого update”.

---

## Что ещё посмотреть

Если хочется быстро понять, как библиотека используется вживую, начните с примеров:

- [examples/blueprint_bot](https://github.com/timoniq/telegrinder/tree/dev/examples/blueprint_bot)
- [examples/with_nodes.py](https://github.com/timoniq/telegrinder/blob/dev/examples/with_nodes.py)
- [examples/keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/keyboard.py)
- [examples/inline_keyboard.py](https://github.com/timoniq/telegrinder/blob/dev/examples/inline_keyboard.py)
- [examples/state_mutator.py](https://github.com/timoniq/telegrinder/blob/dev/examples/state_mutator.py)
- [examples/webhook_bot](https://github.com/timoniq/telegrinder/tree/dev/examples/webhook_bot)

На этом базовый туториал заканчивается. Дальше обычно имеет смысл смотреть примеры и API параллельно с реальной задачей.
