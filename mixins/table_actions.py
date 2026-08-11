from playwright.sync_api import Page, Locator


class TableActionsMixin:
    """Миксин для работы с таблицами"""

    page: Page
    search_input: Locator  # Должен быть определён в дочернем классе

    def search(self, text: str):
        """Поиск по таблице"""
        self.search_input.fill(text)
        self.page.keyboard.press("Enter")
        self.wait_for_timeout(1000)

    def is_row_found(self, text: str) -> bool:
        """Проверить, что строка с текстом есть в таблице"""
        return self.page.locator(f"td:has-text('{text}')").is_visible()

    def open_row(self, text: str):
        """Открыть строку кликом по ссылке внутри td"""
        row = self.page.locator(f"td:has-text('{text}')").first
        link = row.locator("a").first
        if link.count() > 0:
            link.click()
        else:
            row.click()
        self.wait_for_navigation()