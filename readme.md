# async-rabbitmq-py

## Как запустить?

---

Создаем файлы с переменными окружения для контейнеров в докере

```bash
$ touch .env .env.db .env.mq
```

Заполняем содержимым

```py
# .env
DATABASE_URL=postgresql+psycopg2://postgres:postgres@db:5432/rabbitmq
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=user
```

```py
# .env.db
POSTGRES_DB=rabbitmq
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
```

```py
# env.mq
RABBITMQ_DEFAULT_USER=user
RABBITMQ_DEFAULT_PASS=user
```

Запускаем + билдим докер файлы

```bash
$ docker compose up -d --build
# или
$ docker-compose up -d --build
```

Создаем бд и добавляем туда данные

```bash
$ docker compose exec rpc python database/migrations/__make_db__.py
$ docker compose exec rpc python database/migrations/__seed_data__.py
# или
$ docker-compose exec rpc python database/migrations/__make_db__.py
$ docker-compose exec rpc python database/migrations/__seed_data__.py
```

## Подключаемся в качестве клиента

---

Данные для входа по умолчанию, если вы добавляли данные в бд при помощи скрипта

> Имя пользователя: **admin**
> Пароль: **admin**

```bash
$ docker compose exec rpc python client.py
# или
$ docker-compose exec rpc python client.py
```

## Что реализованно?

---

Список вещей которые должны быть реализованны:

- [X] Использовалась реляционная база данных и **ORM SQLAlchemy** с **PostgreSQL**.
- [X] Поддержка асинхронной обработки клиентских запросов с помощью очередей **RabbitMQ**.
- [X] Запуск более **одного** экземпляра сервера был невозможен.
- [X] Пользователь должен уметь **аутентифицироваться**.
- [X] Возможность поиска по **авторам** и **названию**.
