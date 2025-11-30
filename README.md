# Task Tracker CLI

Простой консольный трекер задач без лишнего мусора.
Хранит данные в `tasks.json`, работает без библиотек, только стандартный Python.

## Возможности

* Добавление задач
* Обновление описания
* Удаление
* Изменение статуса:

  * `todo`
  * `in-progress`
  * `done`
* Просмотр всех задач или только выбранного статуса
* Автоматическое создание `tasks.json`
* Безопасная запись (atomic write) — файл не ломается даже при сбоях

## Формат хранения задач (tasks.json)

Каждая задача выглядит так:

```json
{
    "id": 1,
    "description": "Buy milk",
    "status": "todo",
    "createdAt": "2025-11-29T23:38:01.078332Z",
    "updatedAt": "2025-11-29T23:38:01.078332Z"
}
```

## Установка

0. Убедись, что стоит Python 3.
1. Склонируй или скопируй файлы куда хочешь.
2. Готово — ничего больше не нужно.

## Запуск

```
python tracker.py <команда> [аргументы]
```

## Команды

### Добавить задачу

```
python tracker.py add "купить макароны"
```

### Обновить описание

```
python tracker.py update 3 "купить макароны и сыр"
```

### Удалить задачу

```
python tracker.py delete 2
```

### Отметить как in-progress

```
python tracker.py mark-in-progress 1
```

### Отметить как done

```
python tracker.py mark-done 1
```

### Посмотреть все задачи

```
python tracker.py list
```

### Посмотреть только задачи определённого статуса

```
python tracker.py list todo
python tracker.py list in-progress
python tracker.py list done
```

### Помощь

```
python tracker.py help
```

## Как это работает внутри

* Все команды идут через `main()`, который парсит аргументы.
* Все задачи хранятся в JSON-файле.
* Запись идёт через `atomic_write()` → временный файл → безопасная замена.
* Все статусы валидируются.
* Система сама назначает ID.
* Время пишется в UTC в ISO-формате.

## Обработка ошибок

* Неправильные команды → вывод ошибки.
* Неправильный статус → тоже ошибка.
* Пустое описание → ошибка.
* Ломаный JSON игнорируется (файл будет перезаписан нормально при следующей операции).

## Пример работы

```
> python tracker.py add "Buy groceries"
Task added successfully (ID: 1)

> python tracker.py mark-in-progress 1
Task 1 marked in-progress.

> python tracker.py list todo
No tasks.

> python tracker.py list
1. Buy groceries - in-progress (created: ..., updated: ...)
```
