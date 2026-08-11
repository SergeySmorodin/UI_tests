from playwright.sync_api import Page


class DebugMixin:
    """Миксин для отладки"""

    page: Page

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
