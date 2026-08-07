import datetime

from playwright.sync_api import Page, expect, Locator

from config import VPNConfig


class BasePage:
    """Базовый класс для всех страниц"""

    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000

    # === Навигация ===

    def open_url(self, url: str):
        """Открыть страницу по полному URL"""
        self.page.goto(url)
        self.page.wait_for_load_state('networkidle')

    def open_relative(self, config: VPNConfig, path: str = ""):
        """Открыть страницу с относительным путём"""
        url = f"{config.site_url}{path}"
        self.open_url(url)

    def get_current_url(self) -> str:
        """Получить текущий URL"""
        return self.page.url

    def get_title(self) -> str:
        """Получить заголовок страницы"""
        return self.page.title()

    # === Работа с элементами ===

    def wait_for_element(self, locator: Locator, state: str = 'visible', timeout: int = None):
        """Ожидание состояния элемента"""
        timeout = timeout or self.timeout
        locator.wait_for(state=state, timeout=timeout)

    def is_element_visible(self, locator: Locator) -> bool:
        """Проверить, видим ли элемент"""
        try:
            return locator.is_visible()
        except:
            return False

    def click(self, locator: Locator):
        """Кликнуть по элементу"""
        expect(locator).to_be_visible(timeout=self.timeout)
        expect(locator).to_be_enabled(timeout=self.timeout)
        locator.click()

    def fill(self, locator: Locator, text: str):
        """Заполнить поле текстом"""
        expect(locator).to_be_visible(timeout=self.timeout)
        locator.clear()
        locator.fill(text)

    def get_text(self, locator: Locator) -> str:
        """Получить текст элемента"""
        if self.is_element_visible(locator):
            return locator.text_content()
        return ""

    # === Проверки (assertions) ===

    def expect_element_visible(self, locator: Locator):
        """Проверить, что элемент видим"""
        expect(locator).to_be_visible(timeout=self.timeout)

    def expect_url_contains(self, text: str):
        """Проверить, что URL содержит текст"""
        expect(self.page).to_have_url(f"**{text}**", timeout=self.timeout)

    def expect_url_not_contains(self, text: str):
        """Проверить, что URL НЕ содержит текст"""
        expect(self.page).not_to_have_url(f"**{text}**", timeout=self.timeout)

    # === Отладка ===

    def take_screenshot(self, name: str = "screenshot"):
        """Сделать скриншот"""
        import os
        os.makedirs("screenshots", exist_ok=True)
        self.page.screenshot(path=f"screenshots/{name}.png")

    def debug_info(self):
        """Вывести отладочную информацию"""
        print(f"\n=== DEBUG: {self.__class__.__name__} ===")
        print(f"URL: {self.get_current_url()}")
        print(f"Title: {self.get_title()}")

    # === Ожидания ===

    def wait_for_navigation(self):
        """Ожидание завершения навигации"""
        self.page.wait_for_load_state('networkidle')

    def wait_for_timeout(self, milliseconds: int = 1000):
        """Пауза в миллисекундах"""
        self.page.wait_for_timeout(milliseconds)

    # === Вспомогательные методы ===





