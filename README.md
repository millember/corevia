# corevia
Corevia — локальная кроссплатформенная платформа для автоматизации, планирования задач, управления сетью и проксирования
Вот короткий вариант для README:

## Проверяем Docker

Собираем Docker-образ:

```bash
docker compose build
````

Создаёт образ Corevia на основе `Dockerfile.dev`.

Запускаем dev-контейнер в фоне:

```bash
docker compose up -d dev
```

Запускает сервис `dev` и оставляет его работать в фоне.

Проверяем Python внутри контейнера:

```bash
docker compose exec dev \
    uv run python --version
```

Выполняет команду внутри работающего контейнера `dev` и показывает версию Python.

Проверяем Corevia внутри контейнера:

```bash
docker compose exec dev \
    uv run corevia
```

Запускает Corevia внутри Docker.

Ожидаем:

```text
Corevia
```