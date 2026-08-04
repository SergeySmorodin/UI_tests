# Библиотеки
```
# UI тестирование
pytest-playwright

# Фабрика тестовых даанных
factory_boy

# для работы с моками и патчами в pytest
pytest-mock

# для анализа покрытия кода тестами
coverage
pytest-cov

# pytest-плагин для тестирования Django-проектов
pytest-django

# для валидации JSON-структур по схемам
jsonschema

# для параллельного запуска тестов 
pytest-xdist

# для генерации отчетов Allure
allure-pytest
```

# Установка библиотек
```bash
poetry add pytest-playwright factory_boy pytest-mock coverage pytest-cov pytest-django jsonschema pytest-xdist allure-pytest --group dev

playwright install
```

# Необходимо для работы тестов
```

```

# Настройка тестовой БД
``` 

```

# Команды для запуска тестов
#### Запуск всех тестов
* Команда для параллельного запуска всех тестов
```pytest -n auto```
* Подробный вывод с именами тестов и print-ами и открытием страниц в браузере
```pytest -v -s -n auto --headed```

#### Запуск по маркерам
* Запуск тестов по маркерам, используется опция -m <выражение_маркера>
```pytest -m "api" -n auto```
* Запустить тесты, НЕ имеющие маркера (добавить not к маркеру - исключить медленные тесты)
```pytest -m "not slow" -n auto```
* Только модульные тесты (изолированные, с моками)
```pytest -m "units" -n auto```
* Только тесты с Excel
```pytest -m "excel" -n auto```
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
```pytest -k "test_api_projects"```

#### Тесты вложенности сериализаторов (запускается только с флагом deep_serializer)
* Генерацией отчета в serializer_reports
```pytest -m deep_serializer -k test_serializers_fields```

#### Проверка покрытия кода тестами
* Очистка отчетов + запуск тестов + покрытие кода
```coverage erase; Remove-Item -Recurse -Force htmlcov -ErrorAction SilentlyContinue; pytest -n auto --cov=. --cov-config=.coveragerc --cov-report=html --cov-report=term-missing```


#### Генерация отчетов Allure
* Формирование папки с отчетами + запуск сервера allure
```pytest -n auto --alluredir=./allure-results;allure serve ./allure-results```


