from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage


class LoginPage(BasePage):
    """Страница авторизации"""

    PAGE = "login"

    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        """Инициализация локаторов"""
        self.username_input = self.page.locator("#username")
        self.password_input = self.page.locator("#pass")
        self.login_button = self.page.get_by_role("button", name="Вход")
        self.lk_link = self.page.get_by_role("link", name="Личный кабинет")

    def open(self, config: VPNConfig):
        """Открыть страницу логина"""
        super().open(config, self.PAGE, self.username_input)

    def check_login_form_visible(self):
        """Проверить, что форма логина отображается"""
        self.expect_element_visible(self.username_input)
        self.expect_element_visible(self.password_input)
        self.expect_element_visible(self.login_button)

    def fill_credentials(self, username: str, password: str):
        """Заполнить учётные данные"""
        self.fill(self.username_input, username)
        self.fill(self.password_input, password)

    def click_login_button(self):
        """Нажать кнопку входа"""
        self.click(self.login_button)

    def login(self, config: VPNConfig):
        """Выполнить вход с конфигом"""
        self.open(config)
        self.check_login_form_visible()
        self.fill_credentials(config.login, config.password)
        self.click_login_button()
        self.wait_for_navigation()

    def is_login_successful(self) -> bool:
        """Проверить успешность входа"""
        # Ждём либо ухода со страницы логина, либо появления ошибки
        try:
            self.page.wait_for_url(lambda url: "login" not in url.lower(), timeout=5000)
            print(f"✓ Текущий URL: {self.page.url}")
            return True
        except:
            print(f"✗ Всё ещё на странице логина: {self.page.url}")
            error = self.get_error_message()
            if error:
                print(f"Ошибка: {error}")
            return False

    def is_lk_in_page(self) -> bool:
        """Проверить наличие ссылки на личный кабинет"""
        self.wait_for_timeout(1000)

        return self.lk_link.is_visible()
