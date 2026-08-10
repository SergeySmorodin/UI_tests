from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage

PAGE = "TDO/Projects"


class ProjectsPage(BasePage):
    """Страница со списком договоров"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.search_input = self.page.get_by_placeholder("Поиск")
        self.table_rows = self.page.locator("table tbody tr")
        self.first_row = self.table_rows.first

    def open(self, config: VPNConfig):
        """Открыть страницу создания проекта"""
        super().open(config, PAGE, self.search_input)

    def search_project(self, project_number: str):
        """Найти договор по проекта"""
        self.search_input.fill(project_number)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(1000)

    def is_project_found(self, project_number: str) -> bool:
        """Проверить, что договор отображается в таблице"""
        return self.page.locator(f"td:has-text('{project_number}')").is_visible()

    def open_project(self, project_number: str):
        """Открыть договор кликом по строке"""
        self.page.locator(f"td:has-text('{project_number}')").click()
        self.wait_for_navigation()
