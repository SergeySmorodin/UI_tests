import os
import re
import subprocess
import uuid

import allure
import pytest
from playwright.sync_api import sync_playwright

from config import vpn_config


@pytest.fixture(scope="function")
def test_pdf_file():
    """Создать уникальный PDF для каждого теста"""
    os.makedirs("test_files", exist_ok=True)
    file_path = f"test_files/test_{uuid.uuid4().hex[:8]}.pdf"
    with open(file_path, 'wb') as f:
        f.write(b"%PDF-1.4 test file")
    yield file_path
    # Удалить после теста
    if os.path.exists(file_path):
        os.remove(file_path)


@pytest.fixture(scope="session")
def test_config():
    """Фикстура с конфигурацией для всех тестов"""
    return vpn_config


@pytest.fixture(scope="session")
def vpn_connection(test_config):
    """Проверка VPN подключения"""
    # Извлекаем хост из URL для пинга
    host_match = re.search(r'https?://([^/:]+)', test_config.site_url)
    if host_match:
        host = host_match.group(1)
        result = subprocess.run(
            ["ping", "-n", "1", "-w", "2000", host],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            pytest.skip(
                f"VPN не подключен. Хост {host} недоступен. "
                "Подключитесь через OpenVPN GUI."
            )

        print(f"\n✓ VPN подключение активно, хост {host} доступен")

    yield True


@pytest.fixture(scope="session")
def browser(test_config):
    """Запуск браузера с настройками для корпоративной среды"""
    with sync_playwright() as p:
        # Используем значение из конфигурации
        headless_mode = test_config.headless

        browser = p.chromium.launch(
            headless=headless_mode,
            args=[
                '--ignore-certificate-errors',
                '--disable-web-security',
                '--allow-insecure-localhost',
            ]
        )
        yield browser
        browser.close()


@pytest.fixture(scope="function")
def context(browser, test_config):
    """Создание контекста с игнорированием HTTPS ошибок"""
    context = browser.new_context(
        ignore_https_errors=True,
        viewport={'width': 1920, 'height': 1080}
    )
    context.set_default_timeout(test_config.timeout)
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    """Создание новой страницы для теста"""
    page = context.new_page()
    yield page
    page.close()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Хук для создания скриншота при падении теста"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Получаем page из фикстуры, если она есть
        page = item.funcargs.get('page')
        if page:
            screenshot = page.screenshot(full_page=True)
            allure.attach(
                screenshot,
                name="Скриншот при падении теста",
                attachment_type=allure.attachment_type.PNG
            )

# @pytest.fixture(autouse=True)
# def allure_environment(page):
#     """Добавление информации об окружении"""
#     if page:
#         yield
#         # Можно добавить информацию о браузере
#         browser_info = page.evaluate("() => navigator.userAgent")
#         allure.attach(
#             browser_info,
#             name="Browser Info",
#             attachment_type=allure.attachment_type.TEXT
#         )
#
#
# def pytest_configure(config):
#     """Добавление информации об окружении в отчет"""
#     import os
#     import sys
#
#     # Создаем файл environment.properties для Allure
#     allure_dir = config.getoption('--alluredir', default='allure-results')
#     os.makedirs(allure_dir, exist_ok=True)
#
#     with open(f"{allure_dir}/environment.properties", "w") as f:
#         f.write(f"Python={sys.version}\n")
#         f.write(f"Platform={sys.platform}\n")
