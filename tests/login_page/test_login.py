import allure
import pytest

from pages.login_page import LoginPage


@pytest.mark.usefixtures("vpn_connection")
@allure.feature("Авторизация")
class TestLoginPage:

    @allure.story("Форма логина")
    @allure.title("Проверка отображения формы логина")
    @allure.description("Тест проверяет, что форма авторизации отображается корректно")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_form_visibility(self, login_page, test_config):
        """Тест отображения формы логина"""
        with allure.step("Открыть страницу логина"):
            login_page.open(test_config)

        with allure.step("Проверить видимость формы"):
            login_page.check_login_form_visible()

    @allure.story("Успешная авторизация")
    @allure.title("Проверка входа с корректными данными")
    @allure.description("Тест проверяет успешный вход в систему с валидными учетными данными")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_login_successful(self, authenticated_login_page):
        """Тест успешной авторизации"""
        with allure.step("Проверить успешность входа"):
            assert authenticated_login_page.is_login_successful(), "Вход не выполнен успешно"

        with allure.step("Проверить наличие ссылки на личный кабинет"):
            assert authenticated_login_page.is_lk_in_page(), "Ссылка на личный кабинет отсутствует"

    @allure.story("Негативные сценарии")
    @allure.title("Проверка входа с неверным паролем")
    @allure.description("Тест проверяет появление ошибки при вводе неправильного пароля")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_login_with_wrong_password(self, page, test_config):
        """Тест с неверным паролем"""
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(page)
            login_page.open(test_config)

        with allure.step("Ввести логин и неверный пароль"):
            login_page.fill_credentials(test_config.login, "wrong_password")

        with allure.step("Нажать кнопку входа"):
            login_page.click_login_button()
            login_page.wait_for_navigation()

        with allure.step("Проверить результат"):
            error_message = login_page.get_error_message()

            if error_message:
                allure.attach(error_message, "Сообщение об ошибке", allure.attachment_type.TEXT)
            else:
                assert not login_page.is_login_successful(), \
                    "Ожидалась ошибка, но вход выполнен успешно"

    @allure.story("Негативные сценарии")
    @allure.title("Проверка входа с пустыми полями")
    @allure.description("Тест проверяет, что вход невозможен с пустыми учетными данными")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_credentials(self, page, test_config):
        """Тест с пустыми полями"""
        with allure.step("Открыть страницу логина"):
            login_page = LoginPage(page)
            login_page.open(test_config)

        with allure.step("Нажать кнопку входа без заполнения полей"):
            login_page.click_login_button()

        with allure.step("Проверить, что вход не выполнен"):
            assert not login_page.is_login_successful(), \
                "Вход не должен быть выполнен с пустыми полями"
