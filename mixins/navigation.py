from playwright.sync_api import Page, Locator

from config import VPNConfig


class NavigationMixin:
    """Миксин для навигации по страницам"""

    page: Page
    timeout: int

    def open_url(self, url: str):
        """Открыть страницу по полному URL"""
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')

    def open_relative(self, config: VPNConfig, path: str = ""):
        """Открыть страницу с относительным путём"""
        url = f"{config.site_url}{path}"
        self.open_url(url)

    def open(self, config: VPNConfig, page_path: str, title_locator: Locator = None):
        """Открыть страницу и дождаться загрузки"""
        self.config = config
        self.open_relative(config, page_path)
        if title_locator:
            self.wait_for_element(title_locator)
        self.wait_for_timeout(1000)

    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.page.url

    def get_title(self) -> str:
        """Получить заголовок страницы"""
        return self.page.title()

    def wait_for_navigation(self):
        """Ожидание завершения навигации"""
        self.page.wait_for_load_state('networkidle')

    def wait_for_timeout(self, milliseconds: int = 1000):
        """Пауза в миллисекундах"""
        self.page.wait_for_timeout(milliseconds)
