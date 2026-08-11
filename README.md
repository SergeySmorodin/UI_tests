# Библиотеки
```
# UI тестирование
pytest-playwright

# Фабрика тестовых даанных
factory_boy

# для анализа покрытия кода тестами
pytest-cov

# для параллельного запуска тестов 
pytest-xdist

# для генерации отчетов Allure
allure-pytest
```


# Установка библиотек
```poetry add pytest-playwright factory_boy pytest-cov pytest-xdist allure-pytest```

```playwright install```


# Необходимо для работы тестов
### Файл .env в корне каталога
```
SITE_URL=http://example.ru/
LOGIN=xxx
PASSWORD=xxx
BROWSER_HEADLESS=true
DEFAULT_TIMEOUT=3000
```


# Команды для запуска тестов
#### Запуск всех тестов
* Команда для параллельного запуска всех тестов (тесты одного класса последовательно)
```pytest -n auto --dist loadscope```
* Подробный вывод с именами тестов и print-ами и открытием страниц в браузере
```pytest -v -s --headed```


#### Запуск по маркерам
* Показать только xfail тесты
```pytest -v -m xfail -n auto```
* Показать только skipped тесты
```pytest -v -m skip -n auto```
* Все кроме passed тестов
```pytest -v -r fEswxX -n auto```
* Тесты со статусом xpassed (с исправленными багами)
```pytest -rxpassed -n auto```
* Список доступных маркеров
```pytest --markers```


##### Запуск тестов по имени
* Запуск тестов по маске имени
```pytest -k "test_login"```

```pytest test_login.py::test_successful_login```


#### Проверка покрытия кода тестами
* Очистка отчетов + запуск тестов + покрытие кода
```coverage erase; Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue; pytest -n auto --cov=. --cov-config=.coveragerc --cov-report=html --cov-report=term-missing```


#### Генерация отчетов Allure
* Формирование папки с отчетами + запуск сервера allure
```pytest -n auto --alluredir=./allure-results;allure serve ./allure-results```


#### Полезные команды playwright
* Генерация кода Codegen
```playwright codegen demo.playwright.dev/todomvc/#/```
* Доступные опции Codegen
```playwright codegen --help```

