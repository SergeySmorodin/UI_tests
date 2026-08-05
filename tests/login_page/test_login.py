import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage


@pytest.mark.usefixtures("vpn_connection")
class TestLogin:

    def test_successful_login(self, page: Page, test_config):
        """Тест успешной авторизации"""
        login_page = LoginPage(page)
        login_page.login(test_config)

        assert login_page.is_login_successful(), \
            f"Авторизация не выполнена. Текущий URL: {page.url}"
        print(f"✓ Успешная авторизация. URL: {page.url}")

    def test_login_form_visibility(self, page: Page, test_config):
        """Тест отображения формы логина"""
        login_page = LoginPage(page)
        login_page.open(test_config)
        login_page.check_login_form_visible()
        print("✓ Форма логина отображается корректно")

    def test_login_with_wrong_password(self, page: Page, test_config):
        """Тест с неверным паролем"""
        login_page = LoginPage(page)
        login_page.open(test_config)

        login_page.username_input.fill(test_config.login)
        login_page.password_input.fill("wrong_password")
        login_page.click_login_button()

        page.wait_for_load_state('networkidle')
        error_message = login_page.get_error_message()

        if error_message:
            print(f"✓ Получено ожидаемое сообщение об ошибке: {error_message}")
        else:
            assert not login_page.is_login_successful(), \
                "Ожидалась ошибка, но вход выполнен успешно"
            print("✓ Вход не выполнен (как и ожидалось)")

    def test_empty_credentials(self, page: Page, test_config):
        """Тест с пустыми полями"""
        login_page = LoginPage(page)
        login_page.open(test_config)
        login_page.click_login_button()

        assert not login_page.is_login_successful(), \
            "Вход не должен быть выполнен с пустыми полями"
        print("✓ Вход с пустыми полями заблокирован")