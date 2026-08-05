from playwright.sync_api import Page

from base.base_page import BasePage
from config import VPNConfig

# Selectors
USERNAME = "#username"
PASSWORD = "#pass"
LOGIN_BUTTON = "button:has-text('Войти')"


class LoginPage(BasePage):
    """Страница авторизации"""

    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        """Инициализация локаторов"""
        self.username_input = self.page.locator(USERNAME)
        self.password_input = self.page.locator(PASSWORD)
        self.login_button = self.page.get_by_role("button", name="Вход")
        self.error_message = self.page.locator('.error-message, .alert-danger')

    def open(self, config: VPNConfig):
        """Открыть страницу логина"""
        self.open_relative(config, "login")
        # Ждем загрузки формы
        self.wait_for_element(self.username_input)

    def check_login_form_visible(self):
        """Проверить, что форма логина отображается"""
        self.expect_element_visible(self.username_input)
        self.expect_element_visible(self.password_input)
        self.expect_element_visible(self.login_button)

    def fill_credentials(self, config: VPNConfig):
        """Заполнить учетные данные"""
        self.fill(self.username_input, config.login)
        self.fill(self.password_input, config.password)

    def click_login_button(self):
        """Нажать кнопку входа"""
        self.click(self.login_button)

    def login(self, config: VPNConfig):
        """Полный процесс логина"""
        self.open(config)
        self.check_login_form_visible()
        self.fill_credentials(config)
        self.click_login_button()

    def is_login_successful(self) -> bool:
        """Проверить успешность входа"""
        try:
            # Ждем пока URL перестанет содержать "login"
            self.page.wait_for_url("**/!(*login*)", timeout=1000)
            print(f"✓ URL изменился: {self.page.url}")
            return True
        except:
            current_url = self.get_current_url().lower()

            if "login" in current_url:
                error = self.get_error_message()
                if error:
                    print(f"❌ Авторизация не удалась: {error}")
                else:
                    print(f"❌ Авторизация не удалась без сообщения об ошибке")
                return False

            return True

    def get_error_message(self) -> str:
        """Получить сообщение об ошибке"""
        return self.get_text(self.error_message)
