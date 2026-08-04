# test_vpn_login.py
import pytest
from playwright.sync_api import Page, expect
import subprocess
import sys
from config import vpn_config, VPNConfig


@pytest.fixture(scope="session")
def test_config():
    """Фикстура с конфигурацией для всех тестов"""
    return vpn_config


@pytest.fixture(scope="session")
def vpn_connection(test_config):
    """Проверка VPN подключения"""
    import re
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


# Вариант А: Использование фикстуры test_config
def test_login_with_config_fixture(page: Page, test_config: VPNConfig):
    """Тест с использованием конфигурационной фикстуры"""

    page.goto(test_config.site_url)

    # Используем данные из конфигурации
    page.locator('#username').fill(test_config.login)
    page.locator('#pass').fill(test_config.password)
    page.get_by_role("button", name="Вход").click()

    # Ожидание успешной авторизации
    page.wait_for_load_state('networkidle')

    assert "login" not in page.url.lower(), "Авторизация не выполнена"
    print(f"✓ Успешная авторизация с пользователем: {test_config.login}")


# Вариант Б: Использование глобального объекта vpn_config
def test_login_with_global_config(page: Page):
    """Тест с использованием глобальной конфигурации"""
    from config import vpn_config

    page.goto(vpn_config.site_url)
    page.locator('#username').fill(vpn_config.login)
    page.locator('#pass').fill(vpn_config.password)
    page.get_by_role("button", name="Вход").click()

    page.wait_for_load_state('networkidle')
    assert "login" not in page.url.lower()


# Вариант В: Прямое использование переменных окружения в тесте
def test_login_with_env_direct(page: Page):
    """Тест с прямым использованием переменных окружения"""
    import os

    page.goto(os.getenv('VPN_SITE_URL'))
    page.locator('#username').fill(os.getenv('VPN_LOGIN'))
    page.locator('#pass').fill(os.getenv('VPN_PASSWORD'))
    page.get_by_role("button", name="Вход").click()

    page.wait_for_load_state('networkidle')
