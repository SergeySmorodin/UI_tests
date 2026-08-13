from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage


class PersonalAccountPage(BasePage):
    """Личный кабинет"""

    PAGE = "lk"

    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        """Инициализация локаторов"""
        self.title = self.page.get_by_text("Общая информация").first


    def open(self, config: VPNConfig):
        """Открыть страницу личного кабинета"""
        super().open(config, self.PAGE, self.title)
