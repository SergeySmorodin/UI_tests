import pytest
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.login_page import LoginPage
from pages.tdo_page import TdoPage

""" TODO:
3) Дату договора выбрать с помощью календаря
"""


@pytest.mark.usefixtures("vpn_connection")
class TestTDO:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_config):
        """Вход и открытие страницы"""
        login_page = LoginPage(page)
        login_page.login(test_config)
        assert login_page.is_login_successful(), "Не удалось войти"

        self.tdo_page = TdoPage(page)
        self.tdo_page.open(test_config)

    def test_close_button(self, page: Page):
        """Тест кнопки закрытия формы"""
        current_url = page.url

        self.tdo_page.click_close_button()
        self.tdo_page.wait_for_navigation()
        self.tdo_page.wait_for_timeout(1000)

        # Проверяем, что ушли со страницы создания
        assert page.url != current_url, "URL не изменился после закрытия"
        assert "new" not in page.url.lower(), "Всё ещё на странице создания"

    def test_delete_manager(self, page: Page):
        """Тест удаления менеджера"""
        # Добавляем менеджера
        self.tdo_page.select_random_manager()

        # Удаляем
        self.tdo_page.delete_manager()

        # Проверяем, что менеджер удалён (кнопка удаления исчезла)
        assert not self.tdo_page.is_manager_present(), "Менеджер не удалён"

    def test_delete_work_type(self, page: Page):
        """Тест удаления вида работ"""
        # Добавляем вид работ
        self.tdo_page.select_random_work_type()

        # Удаляем
        self.tdo_page.delete_work_type()

        # Проверяем, что вид работ удалён
        assert not self.tdo_page.is_work_type_present(), "Вид работ не удалён"

    def test_create_contract_successfully(self, page: Page, test_pdf_file):
        """Тест успешного создания договора"""

        contract = ContractFactory()

        # Текстовые поля
        self.tdo_page.fill_contract_number(contract.contract_number)
        self.tdo_page.fill_contract_date(contract.contract_date)
        self.tdo_page.fill_contract_sum(contract.amount)

        # Выпадающие списки
        self.tdo_page.select_random_status()
        self.tdo_page.select_random_company()
        self.tdo_page.select_random_manager()
        self.tdo_page.select_random_work_type()

        # Загрузка файла
        self.tdo_page.upload_file(test_pdf_file)

        # Сохраняем
        self.tdo_page.click_safe_button()
        self.tdo_page.wait_for_navigation()
        self.tdo_page.wait_for_timeout(2000)

        assert self.tdo_page.is_contract_saved(), f"Не удалось сохранить договор {contract.contract_number}"
