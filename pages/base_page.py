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

    def open(self, config: VPNConfig, page_path: str, title_locator: Locator = None):
        """Открыть страницу и дождаться загрузки"""
        self.open_relative(config, page_path)
        if title_locator:
            self.wait_for_element(title_locator)
        self.wait_for_timeout(1000)

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

    # === Файл ===
    def upload_file(self, file_path: str):
        """Загрузить файл. Дочерний класс должен определить self.file_upload"""
        self.file_upload.set_input_files(file_path)

    # === Кнопки ===
    def click_safe_button(self):
        """Нажать кнопку Сохранить. Дочерний класс должен определить self.safe_button"""
        self.click(self.safe_button)

    def click_close_button(self):
        """Нажать кнопку Закрыть. Дочерний класс должен определить self.close_button"""
        self.click(self.close_button)

    # === Проверки закрытия/сохранения ===

    def verify_closed(self, current_url: str = None):
        """Проверить, что страница создания/редактирования закрылась"""
        if current_url is None:
            current_url = self.get_current_url()

        self.wait_for_navigation()
        self.wait_for_timeout(1000)

        assert self.page.url != current_url, "URL не изменился после закрытия"
        assert "new" not in self.page.url.lower(), "Всё ещё на странице создания"
        # assert "edit" not in self.page.url.lower(), "Всё ещё на странице редактирования"

    def verify_saved(self):
        """Проверить, что форма сохранена и ушли со страницы создания/редактирования"""
        self.wait_for_navigation()
        self.wait_for_timeout(1000)

        current_url = self.get_current_url()
        assert "new" not in current_url.lower(), "Всё ещё на странице создания"
        # assert "edit" not in current_url.lower(), "Всё ещё на странице редактирования"

    def click_close_and_verify(self):
        """Нажать кнопку Закрыть и проверить, что ушли со страницы"""
        current_url = self.get_current_url()
        self.click_close_button()
        self.verify_closed(current_url)

    def click_save_and_verify(self):
        """Нажать кнопку Сохранить и проверить, что форма сохранена"""
        self.click_safe_button()
        self.verify_saved()

    # === Выпадающие списки ===
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

    # === Сообщения об ошибках ===

    def is_error_message_visible(self, timeout: int = 3000) -> bool:
        """Проверить наличие сообщения об ошибке"""
        error_locator = self.page.locator('.error, .alert, [role="alert"], .invalid-feedback, .text-danger').first
        try:
            self.wait_for_element(error_locator, timeout=timeout)
            return True
        except:
            return False

    def get_error_message_text(self) -> str:
        """Получить текст сообщения об ошибке"""
        error_locator = self.page.locator('.error, .alert, [role="alert"], .invalid-feedback, .text-danger').first
        if self.is_element_visible(error_locator):
            return error_locator.text_content().strip()
        return ""

    def wait_for_error_message(self, timeout: int = None):
        """Дождаться появления сообщения об ошибке"""
        timeout = timeout or self.timeout
        error_locator = self.page.locator('.error, .alert, [role="alert"], .invalid-feedback, .text-danger').first
        self.wait_for_element(error_locator, timeout=timeout)

    def expect_error_message_visible(self):
        """Проверить, что сообщение об ошибке отображается"""
        error_locator = self.page.locator('.error, .alert, [role="alert"], .invalid-feedback, .text-danger').first
        self.expect_element_visible(error_locator)

    # === Проверки (assertions) ===

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
