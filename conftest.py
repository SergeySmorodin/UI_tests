import pytest
from playwright.sync_api import sync_playwright

@pytest.fixture(scope="session")
def browser():
    """
    Запуск браузера с настройками для корпоративной среды
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=False,  # Показывать браузер для отладки
            args=[
                '--ignore-certificate-errors',  # Игнорировать ошибки SSL
                '--disable-web-security',
                '--allow-insecure-localhost',
            ]
        )
        yield browser
        browser.close()
#
@pytest.fixture(scope="function")
def context(browser):
    """
    Создание контекста с игнорированием HTTPS ошибок
    """
    context = browser.new_context(
        ignore_https_errors=True,  # Важно для внутренних сертификатов
        viewport={'width': 1920, 'height': 1080}
    )
    yield context
    context.close()
