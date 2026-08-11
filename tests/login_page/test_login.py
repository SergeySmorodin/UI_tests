import pytest

from pages.login_page import LoginPage


@pytest.mark.usefixtures("vpn_connection")
class TestLoginPage:

    def test_login_form_visibility(self, login_page, test_config):
        """Тест отображения формы логина"""
        login_page.open(test_config)
        login_page.check_login_form_visible()

    def test_login_successful(self, authenticated_login_page):
        """Тест успешной авторизации"""
        assert authenticated_login_page.is_login_successful()

    def test_login_with_wrong_password(self, page, test_config):
        """Тест с неверным паролем"""
        login_page = LoginPage(page)
        login_page.open(test_config)

        login_page.fill_credentials(test_config.login, "wrong_password")
        login_page.click_login_button()
        login_page.wait_for_navigation()

        error_message = login_page.get_error_message()

        if error_message:
            print(f"✓ Получено ожидаемое сообщение об ошибке: {error_message}")
        else:
            assert not login_page.is_login_successful(), \
                "Ожидалась ошибка, но вход выполнен успешно"

    def test_empty_credentials(self, page, test_config):
        """Тест с пустыми полями"""
        login_page = LoginPage(page)
        login_page.open(test_config)
        login_page.click_login_button()

        assert not login_page.is_login_successful(), \
            "Вход не должен быть выполнен с пустыми полями"