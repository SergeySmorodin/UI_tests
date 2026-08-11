
from playwright.sync_api import Locator, expect, Page


class ElementInteractionsMixin:
    """Миксин для работы с элементами страницы"""

    page: Page
    timeout: int

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

    def is_element_enabled(self, locator: Locator) -> bool:
        """Проверить, активен ли элемент"""
        try:
            return locator.is_enabled()
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

    def get_input_value(self, locator: Locator) -> str:
        """Получить значение поля ввода"""
        if self.is_element_visible(locator):
            return locator.input_value()
        return ""
