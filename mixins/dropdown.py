from playwright.sync_api import Page


class DropdownMixin:
    """Миксин для работы с выпадающими списками"""

    page: Page

    def _get_dropdown_options(self, exclude: list = None) -> list:
        """Получить опции из выпадающего списка"""
        if exclude is None:
            exclude = ['Закрыть', 'Сохранить']
        self.wait_for_timeout(500)
        return [b.text_content().strip()
                for b in self.page.locator('button[type="button"]').all()
                if b.is_visible() and b.text_content().strip() not in exclude]

    def close_dropdown(self):
        """Закрыть выпадающий список"""
        self.page.keyboard.press("Escape")
        self.wait_for_timeout(300)
