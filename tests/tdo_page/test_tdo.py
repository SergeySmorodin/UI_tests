import random

import pytest
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.login_page import LoginPage
from pages.tdo_page import TdoPage


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

    def test_create_contract_successfully(self, page: Page):
        """Тест успешного создания договора"""

        # Создаём данные
        contract = ContractFactory()

        # Заполняем текстовые поля
        self.tdo_page.fill_contract_number(contract.contract_number)
        self.tdo_page.fill_contract_date(contract.contract_date)
        self.tdo_page.fill_contract_sum(contract.amount)

        # Статус
        statuses = self.tdo_page.get_status_options()
        print(f"Статусы: {statuses}")
        if statuses:
            self.tdo_page.select_status(random.choice(statuses))

        # Компания
        companies = self.tdo_page.get_company_options()
        print(f"Компании: {companies}")
        if companies:
            self.tdo_page.select_company(random.choice(companies))

        # Менеджер
        self.tdo_page.add_manager()
        managers = self.tdo_page._get_dropdown_options()
        print(f"Менеджеры: {managers}")
        if managers:
            self.tdo_page.select_manager(random.choice(managers))
        self.tdo_page.close_dropdown()

        # Виды работ
        self.tdo_page.add_work_type()
        work_types = self.tdo_page._get_dropdown_options()
        print(f"Виды работ: {work_types}")
        if work_types:
            self.tdo_page.select_work_types([random.choice(work_types)])
        self.tdo_page.close_dropdown()

        # Сохраняем
        self.tdo_page.click_safe_button()
        self.tdo_page.wait_for_navigation()
        self.tdo_page.wait_for_timeout(2000)

        assert self.tdo_page.is_contract_saved(), f"URL: {page.url}"
        print(f"✓ Договор {contract.contract_number} создан")
