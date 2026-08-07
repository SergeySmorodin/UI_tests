import pytest
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.login_page import LoginPage
from pages.tdo_page import TdoPage

""" TODO:
1) Проверить кнопку Закрыть 
2) Кнопку удалить у менеджера и вида работ 
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
