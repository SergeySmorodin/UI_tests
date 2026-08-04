from playwright.sync_api import Page, expect

from config import VPNConfig

# Selectors
USERNAME = "#username"
PASSWORD = "#pass"
LOGIN_BUTTON = "button:has-text('Войти')"


class LoginPage:

    def __init__(self, page: Page):
        self.page = page
        self.username_input = page.locator(USERNAME)
        self.password_input = page.locator(PASSWORD)
        self.login_button = page.get_by_role("button", name="Вход")

    def open(self, config: VPNConfig):
        """Открыть страницу логина"""
        self.page.goto(f'{config.site_url}login')
        # Ждем загрузки формы
        self.username_input.wait_for(state='visible', timeout=10000)

    def check_login_form_visible(self):
        """Проверить, что форма логина отображается"""
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.login_button).to_be_visible()

    def fill_credentials(self, config: VPNConfig):
        """Заполнить учетные данные"""
        self.username_input.fill(config.login)
        self.password_input.fill(config.password)

    def click_login_button(self):
        """Нажать кнопку входа"""
        self.login_button.click()

    def login(self, config: VPNConfig):
        """Полный процесс логина"""
        self.open(config)
        self.check_login_form_visible()
        self.fill_credentials(config)
        self.click_login_button()

    def is_login_successful(self) -> bool:
        """Проверить успешность входа"""
        # Ждем завершения навигации
        self.page.wait_for_load_state('networkidle')
        return "login" not in self.page.url.lower()

    def get_error_message(self):
        """Получить сообщение об ошибке, если есть"""
        error = self.page.locator('.error-message, .alert-danger')
        if error.is_visible():
            return error.text_content()
        return None
