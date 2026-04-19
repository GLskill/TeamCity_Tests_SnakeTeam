# 🐍 TeamCity Tests — SnakeTeam

Проект автоматизированного API-тестирования **TeamCity** на Python.  
Разработан командой **SnakeTeam**.

---

## 🛠 Стек технологий

| Инструмент | Назначение |
|---|---|
| Python 3.11+ | Основной язык |
| pytest | Фреймворк для тестов |
| requests | HTTP-клиент для API |
| pydantic | Валидация моделей данных |
| faker + rstr | Генерация случайных тестовых данных |
| allure-pytest | Отчёты о прогоне тестов |
| pytest-xdist | Параллельный запуск тестов |
| softest | Мягкие ассерты |
| ruff | Линтер / форматтер |

---

## 📁 Структура проекта

```
TeamCity_Tests_SnakeTeam/
├── src/
│   ├── main/                        # Фреймворк (инфраструктурный код)
│   │   ├── classes/
│   │   │   └── api_manager.py       # Единая точка входа для всех Steps
│   │   ├── configs/
│   │   │   └── config.py            # Конфигурация (BASE_URL и др.)
│   │   ├── fixtures/
│   │   │   └── api_fixtures.py      # pytest-фикстуры
│   │   ├── generators/
│   │   │   ├── generating_rule.py   # Правила генерации данных
│   │   │   └── random_data.py       # Генератор случайных данных (Faker, rstr)
│   │   ├── helpers/
│   │   │   └── allure_helpers.py    # Вспомогательные методы для Allure
│   │   ├── models/
│   │   │   ├── base_model.py        # Базовая Pydantic-модель
│   │   │   └── comparison/
│   │   │       ├── model_assertions.py       # Ассерты для моделей
│   │   │       ├── model_comparator.py       # Сравнение моделей
│   │   │       └── model_comparison_config.py # Конфиг сравнения
│   │   ├── requests/
│   │   │   ├── requester.py         # Абстрактный HTTP-клиент
│   │   │   └── skeleton/
│   │   │       ├── endpoint.py      # Enum всех эндпоинтов с моделями
│   │   │       ├── http_request.py  # Базовый HTTP-запрос
│   │   │       └── interfaces/
│   │   │           └── crud_end_interface.py  # CRUD-интерфейс
│   │   ├── specs/
│   │   │   ├── request_specs.py     # Спецификации запросов
│   │   │   └── response_specs.py    # Спецификации ответов
│   │   └── steps/
│   │       └── base_steps.py        # Базовый класс Steps
│   └── tests/                       # Сами тесты (добавляются сюда)
├── requirements.txt                 # Зависимости
├── ruff.toml                        # Конфиг линтера
└── .gitignore
```

---

## ⚙️ Установка проекта (шаг за шагом)

### 1. Клонировать репозиторий

```bash
git clone https://github.com/GLskill/TeamCity_Tests_SnakeTeam.git
cd TeamCity_Tests_SnakeTeam
```

### 2. Убедиться, что Python 3.11+ установлен

```bash
python --version
# должно быть Python 3.11.x или выше
```

Если Python не установлен — скачай с [python.org](https://www.python.org/downloads/).

### 3. Создать и активировать виртуальное окружение

**Windows (PowerShell):**
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

**macOS / Linux:**
```bash
python -m venv .venv
source .venv/bin/activate
```

> ✅ Ты должен увидеть `(.venv)` в начале строки терминала — значит, окружение активно.

### 4. Установить зависимости

```bash
pip install -r requirements.txt
```

