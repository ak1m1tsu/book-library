# rpc-demo

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
```

Запуск клиента

```bash
(env) $ python client.py
```

> Для того чтобы клиент подключился нужно ввести имя пользователя и пароль.  
> Админ:  
> Login: **admin**  
> Password: **admin**

## Что реализованно?

---

Список вещей которые должны быть реализованны:

- [X] Использовалась реляционная база данных и **ORM SQLAlchemy** с **PostgreSQL**.
- [X] Поддержка асинхронной обработки клиентских запросов с помощью очередей **RabbitMQ**.
- [X] Запуск более **одного** экземпляра сервера был невозможен.
- [X] Пользователь должен уметь **аутентифицироваться**.
- [X] Возможность поиска по **авторам** и **названию**.
