import random

from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage
from pages.locators.contract_locators import ContractLocators


class ContractPage(BasePage):
    """Страница создания договора"""

    PAGE = "TDO/Contract/new"

    def __init__(self, page: Page):
        super().__init__(page)
        self.loc = ContractLocators()
        self._init_locators()

    def _init_locators(self):
        self.contract_input = self.page.get_by_placeholder("Введите номер договора")
        self.date_input = self.page.locator(self.loc.DATE_INPUT)
        self.sum_input = self.page.get_by_placeholder("Введите сумму")
        self.status_select = self.page.locator(self.loc.STATUS_SELECT).first
        self.company_button = self.page.locator(self.loc.COMPANY_DROPDOWN_BUTTON)
        self.safe_button = self.page.get_by_role("button", name="Сохранить")
        self.close_button = self.page.get_by_role("button", name="Закрыть")
        self.title = self.page.get_by_text("Создание договора")
        self.file_upload = self.page.locator(self.loc.FILE_UPLOAD)

    def open(self, config: VPNConfig):
        """Открыть страницу создания договора"""
        super().open(config, self.PAGE, self.title)

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
        return [o.get_attribute("value")
                for o in self.status_select.locator('option').all()
                if o.get_attribute("value")]

    def select_random_status(self):
        statuses = self.get_status_options()
        if statuses:
            self.select_status(random.choice(statuses))

    # === Компания ===
    def open_company_dropdown(self):
        self.company_button.click()
        self.wait_for_timeout(700)

    def select_company(self, company: str):
        """Выбрать компанию (список должен быть открыт)"""
        self.page.locator(self.loc.COMPANY_OPTIONS).filter(has_text=company).first.click()

    def select_random_company(self):
        self.open_company_dropdown()
        options = self.page.locator(self.loc.COMPANY_OPTIONS).all()
        visible_options = [opt for opt in options
                           if opt.is_visible()
                           and opt.text_content().strip()
                           and 'Выберите' not in opt.text_content()]
        if visible_options:
            random.choice(visible_options).click()
        self.close_dropdown()

    # === Менеджер ===
    def select_random_manager(self):
        """Добавить случайного менеджера"""
        # Нажимаем "+"
        self.page.locator(self.loc.ADD_MANAGER_BUTTON).click()
        self.wait_for_timeout(700)

        # Ищем строки менеджеров
        manager_rows = self.page.locator(self.loc.MANAGER_ROW)

        if manager_rows.count() > 0:
            # Берём последнюю строку (новую)
            last_row = manager_rows.last

            # Кликаем по кнопке внутри строки
            dropdown_button = last_row.locator('button[type="button"]').first
            dropdown_button.click()
            self.wait_for_timeout(700)

            # Получаем все видимые кнопки и фильтруем
            all_buttons = self.page.locator('button[type="button"]:visible').all()

            exclude = ['Сохранить', 'Закрыть', 'Выберите', 'Добавить', 'Удалить']

            options = [b for b in all_buttons
                       if len(b.text_content().strip()) > 5
                       and not any(e in b.text_content() for e in exclude)]

            # Пропускаем первую опцию (она уже в строке менеджера)
            options = options[1:]

            if options:
                chosen = random.choice(options)
                chosen.click()
                self.wait_for_timeout(300)

    def delete_manager(self):
        """Удалить добавленного менеджера"""
        # Находим кнопку удаления в последней строке менеджера
        manager_rows = self.page.locator(self.loc.MANAGER_ROW)
        if manager_rows.count() > 0:
            last_row = manager_rows.last
            delete_button = last_row.locator(self.loc.DELETE_MANAGER_BUTTON)
            delete_button.click()
            self.wait_for_timeout(300)

    def is_manager_present(self) -> bool:
        """Проверить, есть ли добавленный менеджер"""
        manager_rows = self.page.locator(self.loc.MANAGER_ROW)
        if manager_rows.count() > 0:
            return manager_rows.last.locator(self.loc.DELETE_MANAGER_BUTTON).is_visible()
        return False

    # === Виды работ ===
    def select_random_work_type(self):
        """Добавить случайный вид работ"""
        # Нажимаем "+"
        self.page.locator(self.loc.ADD_WORK_TYPE_BUTTON).click()
        self.wait_for_timeout(700)

        # Ищем строки видов работ
        work_type_rows = self.page.locator(self.loc.WORK_TYPE_ROW)

        if work_type_rows.count() > 0:
            # Берём последнюю строку (новую)
            last_row = work_type_rows.last

            # Находим select внутри строки
            select = last_row.locator('select')

            # Получаем все option
            options = select.locator('option').all()
            values = [opt.get_attribute("value")
                      for opt in options
                      if opt.get_attribute("value")]

            if values:
                random_value = random.choice(values)
                select.select_option(value=random_value)
                self.wait_for_timeout(300)

    def delete_work_type(self):
        """Удалить добавленный вид работ"""
        work_type_rows = self.page.locator(self.loc.WORK_TYPE_ROW)
        if work_type_rows.count() > 0:
            last_row = work_type_rows.last
            delete_button = last_row.locator(self.loc.DELETE_WORK_TYPE_BUTTON)
            delete_button.click()
            self.wait_for_timeout(300)

    def is_work_type_present(self) -> bool:
        """Проверить, есть ли добавленный вид работ"""
        work_type_rows = self.page.locator(self.loc.WORK_TYPE_ROW)
        if work_type_rows.count() > 0:
            return work_type_rows.last.locator(self.loc.DELETE_WORK_TYPE_BUTTON).is_visible()
        return False
