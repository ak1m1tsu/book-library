# server-client

## Как запустить?

---

Настройка виртуального окружения

```bash
$ python3 -m virtualenv env
$ . env/bin/activate
(env) $ pip install -r requirements.txt
```

Создание БД

```bash
(env) $ python ./database/migrations/__make_db__.py
(env) $ python ./database/migrations/__seed_data__.py
```

Запуск сервера

```bash
(env) $ python server.py
Server started
Waiting for connection...
```

Запуск клиента

```bash
(env) $ python client.py
```

Для того чтобы клиент подключился нужно ввести имя пользователя и пароль.  

```bash
Enter username: admin
Enter password: admin
Checks inputs...
Connected to server as admin
...
```

## Что реализованно?

---

Список вещей которые должны быть реализованны:

- [X] Использовалась реляционная база данных и **ORM SQLAlchemy** с **SQLite**.
- [ ] Поддержка асинхронной обработки клиентских запросов с помощью очередей **RabbitMQ**.
- [X] Запуск более **одного** экземпляра сервера был невозможен.
- [ ] 2 вида клиентов: *админ и пользователь*. **Админ** должен умеет выключать других клиентов и сервер.
