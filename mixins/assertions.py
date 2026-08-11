from playwright.sync_api import Locator, expect, Page


class AssertionsMixin:
    """Миксин для проверок (assertions)"""

    page: Page
    timeout: int

    def expect_element_visible(self, locator: Locator):
        """Проверить, что элемент видим"""
        expect(locator).to_be_visible(timeout=self.timeout)

    def expect_element_not_visible(self, locator: Locator):
        """Проверить, что элемент не видим"""
        expect(locator).not_to_be_visible(timeout=self.timeout)

    def expect_element_enabled(self, locator: Locator):
        """Проверить, что элемент активен"""
        expect(locator).to_be_enabled(timeout=self.timeout)

    def expect_url_contains(self, text: str):
        """Проверить, что URL содержит текст"""
        expect(self.page).to_have_url(f"**{text}**", timeout=self.timeout)

    def expect_url_not_contains(self, text: str):
        """Проверить, что URL НЕ содержит текст"""
        expect(self.page).not_to_have_url(f"**{text}**", timeout=self.timeout)

    def expect_text_on_page(self, text: str):
        """Проверить, что текст присутствует на странице"""
        expect(self.page.get_by_text(text).first).to_be_visible(timeout=self.timeout)
