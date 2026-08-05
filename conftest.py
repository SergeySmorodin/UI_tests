import re
import subprocess

import pytest
from playwright.sync_api import sync_playwright

from config import vpn_config


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
