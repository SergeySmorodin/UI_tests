from playwright.sync_api import Locator, Page


class ErrorHandlingMixin:
    """Миксин для работы с сообщениями об ошибках"""

    page: Page
    timeout: int
    error_message: Locator

    def is_error_message_visible(self, timeout: int = 3000) -> bool:
        """Проверить наличие сообщения об ошибке"""
        try:
            self.wait_for_element(self.error_message, timeout=timeout)
            return True
        except:
            return False

    def get_error_message_text(self) -> str:
        """Получить текст сообщения об ошибке"""
        if self.is_element_visible(self.error_message):
            return self.error_message.text_content().strip()
        return ""

    def wait_for_error_message(self, timeout: int = None):
        """Дождаться появления сообщения об ошибке"""
        timeout = timeout or self.timeout
        self.wait_for_element(self.error_message, timeout=timeout)

    def expect_error_message_visible(self):
        """Проверить, что сообщение об ошибке отображается"""
        self.expect_element_visible(self.error_message)
