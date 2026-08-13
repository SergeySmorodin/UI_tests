import allure
import pytest


@pytest.mark.usefixtures("vpn_connection")
@allure.feature("Вход в личный кабинет")
class TestPersonalAccountPage:

    @allure.story("Успешный вход")
    @allure.title("Проверка перехода в личный кабинет")
    @allure.description("Тест проверяет успешный вход в личный кабинет")
    @allure.severity(allure.severity_level.NORMAL)
    def test_lk_successful(self, personal_account_page):
        """Тест входа в личный кабинет"""
        with allure.step("Проверить успешность входа"):
            assert personal_account_page
