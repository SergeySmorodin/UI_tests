import random
from playwright.sync_api import Page
from config import VPNConfig
from pages.base_page import BasePage

PAGE = "TDO/Contract/new"


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
        self.safe_button = self.page.locator('[type="submit"]')
        self.title = self.page.get_by_text("Создание договора")
        self.file_upload = self.page.locator("input[type='file']")

    def open(self, config: VPNConfig):
        self.open_relative(config, PAGE)
        self.wait_for_element(self.title)
        self.wait_for_timeout(1000)

    # === Текстовые поля ===
    def fill_contract_number(self, number: str): self.contract_input.fill(number)
    def fill_contract_date(self, date: str): self.date_input.fill(date)
    def fill_contract_sum(self, amount: str): self.sum_input.fill(str(amount))

    # === Статус ===
    def select_status(self, status: str):
        self.status_select.select_option(label=status)

    def get_status_options(self) -> list:
        return [o.text_content().strip() for o in self.status_select.locator('option').all()
                if o.text_content().strip()]

    def select_random_status(self):
        statuses = self.get_status_options()
        if statuses:
            self.select_status(random.choice(statuses))

    # === Компания ===
    def open_company_dropdown(self):
        self.company_button.click()
        self.wait_for_timeout(500)

    def select_company(self, company: str):
        """Выбрать компанию (список должен быть уже открыт)"""
        self.page.locator('button[type="button"]').filter(has_text=company).first.click()
        print(f"✓ Компания: {company}")

    def select_random_company(self):
        self.open_company_dropdown()
        companies = self._get_dropdown_options(exclude=['Выберите компанию'])
        if companies:
            self.select_company(random.choice(companies))
        self.close_dropdown()

    # === Менеджер ===
    def open_manager_dropdown(self):
        """Нажать + для добавления менеджера"""
        self.page.locator('button[title="Добавить менеджера"]').click()
        self.wait_for_timeout(500)

    # def select_manager(self, manager: str):
    #     """Выбрать менеджера из выпадающего списка"""
    #     option = self.page.locator(f'li:has-text("{manager}"), [role="option"]:has-text("{manager}")').first
    #     if option.is_visible():
    #         option.click()

    def select_random_manager(self):
        """Добавить случайного менеджера"""
        self.open_manager_dropdown()
        # Кликаем по появившейся строке, чтобы открыть список
        manager_row = self.page.locator("text=Менеджеры").locator("..").locator("input, [role='combobox']")
        if manager_row.count() > 0:
            manager_row.click()
            self.wait_for_timeout(500)
            options = [o for o in self.page.locator('li, [role="option"]').all() if o.is_visible()]
            if options:
                random.choice(options).click()

    # === Виды работ ===
    def open_work_type_dropdown(self):
        """Нажать + для добавления вида работ"""
        self.page.locator('button[title="Добавить вид работ"]').click()
        self.wait_for_timeout(500)

    # def select_work_type(self, work_type: str):
    #     """Выбрать вид работ"""
    #     option = self.page.locator(f'li:has-text("{work_type}"), [role="option"]:has-text("{work_type}")').first
    #     if option.is_visible():
    #         option.click()

    def select_random_work_type(self):
        """Добавить случайный вид работ"""
        self.open_work_type_dropdown()
        work_row = self.page.locator("text=Виды работ").locator("..").locator("input, [role='combobox']")
        if work_row.count() > 0:
            work_row.click()
            self.wait_for_timeout(500)
            options = [o for o in self.page.locator('li, [role="option"]').all() if o.is_visible()]
            if options:
                random.choice(options).click()

    # === Файл ===
    def upload_file(self, file_path: str): self.file_upload.set_input_files(file_path)

    # === Сохранение ===
    def click_safe_button(self): self.safe_button.click()
    def is_contract_saved(self) -> bool: return "new" not in self.get_current_url().lower()

    # === Вспомогательные ===
    def _get_dropdown_options(self, exclude: list = None) -> list:
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
