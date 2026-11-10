# kubeaudit

Учебный pet проект без вайбкодинга для изучения Python. Проверяет ресурсы на latest образ, отсутствие лимитов и readness probe у контейнеров.

## Проверки

| check_id | Что ищет | Severity |
|---|---|---|
| `image-latest-tag` | образ с тегом `latest` или без тега | warning |
| `missing-limits` | контейнер без `resources.limits` | warning |
| `missing-readiness-probe` | основной контейнер без `readinessProbe` | warning |

## Структура

```
src/kubeaudit/
  models.py   # Severity, Finding
  checks.py   # get_pod_spec, get_containers, проверки
tests/
  test_checks.py
```

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Тесты и форматирование

```bash
pytest -v
ruff format .
ruff check .
```

## Запуск

```bash
kind create cluster --name kubeaudit
kubectl apply -f demo/deployments.yaml
python -m kubeaudit.scanner
```