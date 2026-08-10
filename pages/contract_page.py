import random

from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage
from pages.locators.tdo_locators import TdoLocators

PAGE = "TDO/Contract/new"


class TdoPage(BasePage):
    """Страница создания договора"""

    def __init__(self, page: Page):
        super().__init__(page)
        self.loc = TdoLocators()
        self._init_locators()

    def _init_locators(self):
        self.contract_input = self.page.get_by_placeholder("Введите номер договора")
        self.date_input = self.page.locator(self.loc.DATE_INPUT)
        self.sum_input = self.page.get_by_placeholder("Введите сумму")
        self.status_select = self.page.locator(self.loc.STATUS_SELECT).first
        self.company_button = self.page.get_by_role("button", name="Выберите компанию")
        self.safe_button = self.page.get_by_role("button", name="Сохранить")
        self.close_button = self.page.get_by_role("button", name="Закрыть")
        self.title = self.page.get_by_text("Создание договора")
        self.file_upload = self.page.locator(self.loc.FILE_UPLOAD)

    def open(self, config: VPNConfig):
        """Открыть страницу создания договора"""
        super().open(config, PAGE, self.title)

    def fill_form(self, contract, test_pdf_file: str):
        """Заполнить все поля формы"""
        self.fill_contract_number(contract.contract_number)
        self.fill_contract_date(contract.contract_date)
        self.fill_contract_sum(contract.amount)
        self.select_random_status()
        self.select_random_company()
        self.select_random_manager()
        self.select_random_work_type()
        self.upload_file(test_pdf_file)

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
        selector, filter_kwargs = self.loc.company_by_name(company)
        self.page.locator(selector).filter(**filter_kwargs).first.click()

    def select_random_company(self):
        self.open_company_dropdown()
        companies = self._get_dropdown_options(exclude=['Выберите компанию'])
        if companies:
            self.select_company(random.choice(companies))
        self.close_dropdown()

    # === Менеджер ===
    def open_manager_dropdown(self):
        """Нажать + для добавления менеджера"""
        self.page.locator(self.loc.ADD_MANAGER_BUTTON).click()
        self.wait_for_timeout(500)

    def select_random_manager(self):
        """Добавить случайного менеджера"""
        self.open_manager_dropdown()
        manager_row = self.page.locator(self.loc.section_input("Менеджеры"))
        if manager_row.count() > 0:
            manager_row.click()
            self.wait_for_timeout(500)
            options = [o for o in self.page.locator(self.loc.DROPDOWN_OPTIONS).all() if o.is_visible()]
            if options:
                random.choice(options).click()

    def delete_manager(self):
        """Удалить добавленного менеджера"""
        self.page.locator(self.loc.DELETE_MANAGER_BUTTON).click()
        self.wait_for_timeout(300)

    def is_manager_present(self) -> bool:
        """Проверить, есть ли добавленный менеджер"""
        return self.page.locator(self.loc.DELETE_MANAGER_BUTTON).is_visible()

    # === Виды работ ===
    def open_work_type_dropdown(self):
        """Нажать + для добавления вида работ"""
        self.page.locator(self.loc.ADD_WORK_TYPE_BUTTON).click()
        self.wait_for_timeout(500)

    def select_random_work_type(self):
        """Добавить случайный вид работ"""
        self.open_work_type_dropdown()
        work_row = self.page.locator(self.loc.section_input("Виды работ"))
        if work_row.count() > 0:
            work_row.click()
            self.wait_for_timeout(500)
            options = [o for o in self.page.locator(self.loc.DROPDOWN_OPTIONS).all() if o.is_visible()]
            if options:
                random.choice(options).click()

    def delete_work_type(self):
        """Удалить добавленный вид работ"""
        self.page.locator(self.loc.DELETE_WORK_TYPE_BUTTON).click()
        self.wait_for_timeout(300)

    def is_work_type_present(self) -> bool:
        """Проверить, есть ли добавленный вид работ"""
        return self.page.locator(self.loc.DELETE_WORK_TYPE_BUTTON).is_visible()
