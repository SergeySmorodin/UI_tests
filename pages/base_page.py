from playwright.sync_api import Page, Locator

from config import VPNConfig
from mixins.assertions import AssertionsMixin
from mixins.debug import DebugMixin
from mixins.dropdown import DropdownMixin
from mixins.element_interactions import ElementInteractionsMixin
from mixins.error_handling import ErrorHandlingMixin
from mixins.navigation import NavigationMixin
from mixins.table_actions import TableActionsMixin


class BasePage(
    NavigationMixin,
    ElementInteractionsMixin,
    DropdownMixin,
    ErrorHandlingMixin,
    AssertionsMixin,
    TableActionsMixin,
    DebugMixin
):
    """Базовый класс для всех страниц"""

    PAGE: str = ""  # Должен быть переопределён в дочерних классах

    def __init__(self, page: Page):
        self.page = page
        self.timeout = 10000

    @classmethod
    def open_page(cls, page: Page, config: VPNConfig, title_locator: Locator = None):
        """
        Фабричный метод: создать экземпляр страницы и открыть её.

        Использует open() из NavigationMixin.

        Usage:
            contracts_page = ContractsPage.open_page(page, test_config)
            projects_page = ProjectsPage.open_page(page, test_config)
        """
        instance = cls(page)
        instance.open(config, cls.PAGE, title_locator)  # open() из NavigationMixin
        return instance

    # === Файл ===
    def upload_file(self, file_path: str):
        """Загрузить файл"""
        self.file_upload.set_input_files(file_path)

    # === Кнопки ===
    def click_safe_button(self):
        """Нажать кнопку Сохранить"""
        self.click(self.safe_button)

    def click_close_button(self):
        """Нажать кнопку Закрыть"""
        self.click(self.close_button)

    # === Проверки закрытия/сохранения ===
    def verify_closed(self, current_url: str = None):
        """Проверить, что страница закрылась"""
        if current_url is None:
            current_url = self.get_current_url()

        self.wait_for_navigation()
        self.wait_for_timeout(1000)

        assert self.page.url != current_url, "URL не изменился после закрытия"
        assert "new" not in self.page.url.lower(), "Всё ещё на странице создания"

    def verify_saved(self):
        """Проверить, что форма сохранена"""
        self.wait_for_navigation()
        self.wait_for_timeout(1000)

        current_url = self.get_current_url()
        assert "new" not in current_url.lower(), "Всё ещё на странице создания"

    def click_close_and_verify(self):
        """Нажать Закрыть и проверить"""
        current_url = self.get_current_url()
        self.click_close_button()
        self.verify_closed(current_url)

    def click_save_and_verify(self):
        """Нажать Сохранить и проверить"""
        self.click_safe_button()
        self.verify_saved()
