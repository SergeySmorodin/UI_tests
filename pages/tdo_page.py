
from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage


class TdoPage(BasePage):
    """Страница создания договора"""

    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        self.contract_input = self.page.get_by_placeholder("Введите номер договора")
        self.date_input = self.page.locator("#contract_date")
        self.sum_input = self.page.get_by_placeholder("Введите сумму")
        self.status_select = self.page.locator("select, combobox").first
        self.company_button = self.page.get_by_role("button", name="Выберите компанию")
        self.safe_button = self.page.get_by_role("button", name="Сохранить")
        self.title = self.page.get_by_text("Создание договора")
        self.file_upload = self.page.locator("input[type='file']")

    def open(self, config: VPNConfig):
        self.open_relative(config, "TDO/Contract/new")
        self.wait_for_element(self.title)
        self.wait_for_timeout(1000)

    # === Текстовые поля ===
    def fill_contract_number(self, number: str):
        self.contract_input.fill(number)

    def fill_contract_date(self, date: str):
        self.date_input.fill(date)

    def fill_contract_sum(self, amount: str):
        self.sum_input.fill(str(amount))

    # === Статус ===
    def select_status(self, status: str):
        self.status_select.select_option(label=status)

    def get_status_options(self) -> list:
        return [o.text_content().strip() for o in self.status_select.locator('option').all() if
                o.text_content().strip()]

    # === Компания ===
    def open_company_dropdown(self):
        self.company_button.click()
        self.wait_for_timeout(700)

    def select_company(self, company: str):
        self.open_company_dropdown()
        self.page.locator(f'button[type="button"]:has-text("{company}")').first.click()

    def get_company_options(self) -> list:
        self.open_company_dropdown()
        companies = self._get_dropdown_options(exclude=['Закрыть', 'Сохранить', 'Выберите компанию'])
        self.close_dropdown()
        return companies

    # === Менеджер ===
    def add_manager(self):
        self.page.get_by_text("Менеджеры").locator("..").locator("button").click()
        self.wait_for_timeout(500)

    def select_manager(self, manager: str):
        self.page.locator(f'button[type="button"]:has-text("{manager}")').first.click()

    def get_manager_options(self) -> list:
        self.add_manager()
        managers = self._get_dropdown_options()
        self.close_dropdown()
        return managers

    # === Виды работ ===
    def add_work_type(self):
        self.page.get_by_text("Виды работ").locator("..").locator("button").click()
        self.wait_for_timeout(500)

    def select_work_types(self, work_types: list):
        for wt in work_types:
            self.page.locator(f'button[type="button"]:has-text("{wt}")').first.click()

    def get_work_types_options(self) -> list:
        self.add_work_type()
        work_types = self._get_dropdown_options()
        self.close_dropdown()
        return work_types

    # === Файл ===
    def upload_file(self, file_path: str):
        self.file_upload.set_input_files(file_path)

    # === Сохранение ===
    def click_safe_button(self):
        self.safe_button.click()

    def is_contract_saved(self) -> bool:
        return "new" not in self.get_current_url().lower()

    # === Вспомогательные ===
    def _get_dropdown_options(self, exclude: list = None) -> list:
        if exclude is None:
            exclude = ['Закрыть', 'Сохранить']
        self.wait_for_timeout(500)
        return [b.text_content().strip()
                for b in self.page.locator('button[type="button"]').all()
                if b.is_visible() and b.text_content().strip() not in exclude]

    def close_dropdown(self):
        self.page.locator('body').click(position={'x': 0, 'y': 0})
        self.wait_for_timeout(300)