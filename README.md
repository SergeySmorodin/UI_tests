# Библиотеки
```
# UI тестирование
pytest-playwright

# Фабрика тестовых даанных
factory_boy

# для параллельного запуска тестов 
pytest-xdist

# для генерации отчетов Allure
allure-pytest
```


# Установка библиотек
```poetry add pytest-playwright factory_boy pytest-xdist allure-pytest```

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


# Генерация отчетов Allure локально
* Формирование папки с отчетами + запуск сервера allure
```pytest -n auto --dist loadscope --alluredir=./allure-results;allure serve ./allure-results```
* Запуск тестов с сохранением результатов
```pytest --alluredir=./allure-results```
* Или с дополнительными опциями
```pytest --alluredir=./allure-results -v --clean-alluredir```
* Просмотр отчета
```allure serve ./allure-results```
* Генерация статического отчета
```allure generate ./allure-results -o ./allure-report --clean```


# Публикация отчетов Allure на гитхаб
* Полный цикл: тесты → отчёт → публикация → открыть в браузере
```python publish_allure.py```
* Только тесты и отчёт (без публикации)
```python allure_publisher.py --no-publish```
* Только отчёт из готовых результатов (тесты уже были)
```python allure_publisher.py --skip-tests```
* Тесты + отчёт, без открытия браузера
```python allure_publisher.py --no-browser```
* Только отчёт локально, без тестов и без публикации
```python allure_publisher.py --skip-tests --no-publish```
* С другим репозиторием
```python allure_publisher.py --repo-url https://github.com/username/repo.git```


#### Полезные команды playwright
* Генерация кода Codegen
```playwright codegen demo.playwright.dev/todomvc/#/```
* Доступные опции Codegen
```playwright codegen --help```

