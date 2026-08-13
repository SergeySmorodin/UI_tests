import os
import platform
import re
import subprocess
import sys
import uuid
from datetime import datetime

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


########################## Настройка Allure ##############################################################


@pytest.fixture(autouse=True)
def allure_environment(page):
    """Добавление информации об окружении в каждый тест"""
    if page:
        # Добавляем информацию до выполнения теста
        allure.attach(
            f"Test started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            name="Test Start Time",
            attachment_type=allure.attachment_type.TEXT
        )

        yield

        # Добавляем информацию после выполнения теста
        try:
            # Информация о браузере
            browser_info = page.evaluate("() => navigator.userAgent")
            allure.attach(
                browser_info,
                name="Browser Info",
                attachment_type=allure.attachment_type.TEXT
            )
            # Информация о разрешении экрана
            screen_size = page.evaluate("() => ({width: window.screen.width, height: window.screen.height})")
            allure.attach(
                f"Width: {screen_size['width']}, Height: {screen_size['height']}",
                name="Screen Resolution",
                attachment_type=allure.attachment_type.TEXT
            )
            # Информация о URL
            current_url = page.url
            allure.attach(
                current_url,
                name="Current URL",
                attachment_type=allure.attachment_type.TEXT
            )
            # Информация о времени выполнения
            allure.attach(
                f"Test finished at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
                name="Test End Time",
                attachment_type=allure.attachment_type.TEXT
            )

        except Exception as e:
            allure.attach(
                f"Error getting browser info: {str(e)}",
                name="Browser Info Error",
                attachment_type=allure.attachment_type.TEXT
            )


def pytest_configure(config):
    """Добавление информации об окружении в отчет Allure"""

    allure_dir = config.getoption('--alluredir', default=None)
    if allure_dir is None:
        allure_dir = 'allure-results'
    os.makedirs(allure_dir, exist_ok=True)

    # Записываем environment.properties
    with open(os.path.join(allure_dir, "environment.properties"), "w", encoding='utf-8') as f:
        f.write(f"Python Version={sys.version}\n")
        f.write(f"Python Executable={sys.executable}\n")
        f.write(f"Platform={sys.platform}\n")
        f.write(f"OS={platform.system()}\n")
        f.write(f"OS Version={platform.version()}\n")
        f.write(f"Machine={platform.machine()}\n")
        f.write(f"Processor={platform.processor()}\n")
        f.write(f"Hostname={platform.node()}\n")
        f.write(f"Test Start Time={datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")



@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Добавление скриншотов при падении теста"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        # Получаем page из фикстуры
        page = item.funcargs.get('page')
        if page:
            try:
                # Делаем скриншот при падении
                screenshot = page.screenshot(full_page=True)
                allure.attach(
                    screenshot,
                    name="Failure Screenshot",
                    attachment_type=allure.attachment_type.PNG
                )

                # Сохраняем HTML при падении
                html_content = page.content()
                allure.attach(
                    html_content,
                    name="Page HTML on failure",
                    attachment_type=allure.attachment_type.HTML
                )

                # Логи консоли браузера
                console_messages = page.evaluate("() => window.console.logs || []")
                if console_messages:
                    allure.attach(
                        "\n".join(console_messages),
                        name="Console Logs",
                        attachment_type=allure.attachment_type.TEXT
                    )

            except Exception as e:
                allure.attach(
                    f"Failed to capture failure artifacts: {str(e)}",
                    name="Artifact Capture Error",
                    attachment_type=allure.attachment_type.TEXT
                )
