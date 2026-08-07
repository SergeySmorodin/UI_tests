import random

from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage

PAGE = "TDO/Contracts"


from playwright.sync_api import Page
from config import VPNConfig
from pages.base_page import BasePage


class ContractsPage(BasePage):
    """Страница со списком договоров"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = self.page.get_by_placeholder("Поиск")
        self.table_rows = self.page.locator("table tbody tr")
        self.first_row = self.table_rows.first

    def open(self, config: VPNConfig):
        self.open_relative(config, PAGE)
        self.wait_for_timeout(1000)

    def search_contract(self, contract_number: str):
        """Найти договор по номеру"""
        self.search_input.fill(contract_number)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(1000)

    def is_contract_found(self, contract_number: str) -> bool:
        """Проверить, что договор отображается в таблице"""
        return self.page.locator(f"td:has-text('{contract_number}')").is_visible()

    def open_contract(self, contract_number: str):
        """Открыть договор кликом по строке"""
        self.page.locator(f"td:has-text('{contract_number}')").click()
        self.wait_for_navigation()
