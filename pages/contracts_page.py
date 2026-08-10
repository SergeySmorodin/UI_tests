from playwright.sync_api import Page

from pages.base_page import BasePage


class ContractsPage(BasePage):
    PAGE = "TDO/Contracts"

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = self.page.get_by_placeholder("Поиск")
