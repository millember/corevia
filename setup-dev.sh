#!/usr/bin/env bash

set -euo pipefail

PROJECT_ROOT="$(git rev-parse --show-toplevel)"
cd "$PROJECT_ROOT"

echo "Проверяем необходимые программы..."

command -v git >/dev/null 2>&1 || {
    echo "Ошибка: Git не установлен."
    exit 1
}

command -v uv >/dev/null 2>&1 || {
    echo "Ошибка: uv не установлен."
    exit 1
}

command -v docker >/dev/null 2>&1 || {
    echo "Ошибка: Docker не установлен."
    exit 1
}

docker compose version >/dev/null 2>&1 || {
    echo "Ошибка: Docker Compose недоступен."
    exit 1
}

echo "Устанавливаем Python-зависимости..."
uv sync --locked

echo "Устанавливаем pre-commit hook..."
uv run pre-commit install --hook-type pre-commit

echo "Проверяем все файлы..."
uv run pre-commit run --all-files

echo "Собираем Docker image..."
docker compose build

echo "Запускаем проверки в Docker..."
docker compose run --rm test

echo
echo "Настройка завершена."
echo "Pre-commit hook установлен."
echo "Docker-окружение готово."
