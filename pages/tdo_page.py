from datetime import datetime

from base.base_page import BasePage
from playwright.sync_api import Page

from config import VPNConfig

# Selectors
CONTRACT = "#contract"
DATE_CONTRACT = "#contract_date"
SAFE_BUTTON = "button:has-text('Сохранить')"
TITLE = "Создание договора"


class TdoPage(BasePage):
    """Страница создания договора"""

    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        """Инициализация локаторов"""
        self.contract_input = self.page.locator(CONTRACT)
        self.date_input = self.page.locator(DATE_CONTRACT)
        self.safe_button = self.page.get_by_role("button", name="Сохранить")
        self.title = self.page.get_by_text(TITLE)
        self.error_message = self.page.locator('.error-message, .alert-danger')
        self.success_message = self.page.locator('.success-message, .alert-success')

    def open(self, config: VPNConfig):
        """Открыть страницу создания договора"""
        self.open_relative(config, "TDO/Contract/new")
        self.wait_for_element(self.title)

    def check_tdo_form_visible(self):
        """Проверить, что форма создания договора отображается"""
        self.expect_element_visible(self.contract_input)
        self.expect_element_visible(self.date_input)
        self.expect_element_visible(self.safe_button)
        return True

    def fill_contract_form(self, contract_number: str = None, contract_date: str = None):
        """
        Заполнить форму договора

        Args:
            contract_number: Номер договора (по умолчанию автосгенерированный)
            contract_date: Дата договора в формате YYYY-MM-DD (для type="date")
                          или DD.MM.YYYY (автоматически конвертируется)
        """
        if contract_number is None:
            contract_number = f"TEST-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        if contract_date is None:
            # Для type="date" нужен формат YYYY-MM-DD
            contract_date = datetime.now().strftime('%Y-%m-%d')
        else:
            # Конвертируем DD.MM.YYYY в YYYY-MM-DD если нужно
            contract_date = self._normalize_date(contract_date)

        # Заполняем поля
        self.fill(self.contract_input, contract_number)

        # Для полей type="date" используем fill с правильным форматом
        self.fill(self.date_input, contract_date)

        print(f"✓ Заполнена форма договора: номер={contract_number}, дата={contract_date}")

        return contract_number, self._format_date_display(contract_date)

    def _normalize_date(self, date_str: str) -> str:
        """
        Нормализация даты в формат YYYY-MM-DD

        Принимает форматы:
        - DD.MM.YYYY -> YYYY-MM-DD
        - YYYY-MM-DD -> YYYY-MM-DD (без изменений)
        """
        # Если уже в формате YYYY-MM-DD
        if len(date_str) == 10 and date_str[4] == '-' and date_str[7] == '-':
            return date_str

        # Конвертация из DD.MM.YYYY
        try:
            if '.' in date_str:
                day, month, year = date_str.split('.')
                return f"{year}-{month}-{day}"

            if '/' in date_str:
                day, month, year = date_str.split('/')
                return f"{year}-{month}-{day}"
        except:
            pass

        # Если не удалось распознать - возвращаем как есть
        return date_str

    def _format_date_display(self, date_str: str) -> str:
        """Форматирование даты для отображения (DD.MM.YYYY)"""
        try:
            if '-' in date_str:
                year, month, day = date_str.split('-')
                return f"{day}.{month}.{year}"
        except:
            pass
        return date_str

    def fill_date_with_datepicker(self, date_str: str = None):
        """
        Альтернативный способ заполнения даты через datepicker
        Использовать, если fill() не работает с type="date"
        """
        if date_str is None:
            date_str = datetime.now().strftime('%d.%m.%Y')

        # Кликаем по полю для открытия datepicker
        self.date_input.click()
        self.wait_for_timeout(500)

        # Очищаем поле (выделяем всё и удаляем)
        self.date_input.press('Control+a')
        self.date_input.press('Delete')

        # Вводим дату в формате DD.MM.YYYY (без точек, как числа)
        if '.' in date_str:
            day, month, year = date_str.split('.')
            date_numbers = f"{day}{month}{year}"
        else:
            date_numbers = date_str.replace('-', '')

        self.date_input.fill(date_numbers)
        self.date_input.press('Enter')

    def click_safe_button(self):
        """Нажать кнопку сохранить"""
        self.click(self.safe_button)
        print("✓ Кнопка 'Сохранить' нажата")

    def save_contract(self, contract_number: str = None, contract_date: str = None):
        """
        Полный процесс создания договора

        Returns:
            tuple: (номер договора, дата договора для отображения)
        """
        contract_number, contract_date_display = self.fill_contract_form(
            contract_number, contract_date
        )
        self.click_safe_button()
        self.wait_for_navigation()
        self.wait_for_timeout(2000)
        return contract_number, contract_date_display

    def is_contract_saved(self) -> bool:
        """Проверить, что договор сохранен"""
        current_url = self.get_current_url().lower()
        return "new" not in current_url

    def is_success_message_displayed(self) -> bool:
        """Проверить, отображается ли сообщение об успехе"""
        return self.is_element_visible(self.success_message)

    def get_error_message(self) -> str:
        """Получить сообщение об ошибке"""
        return self.get_text(self.error_message)

    def get_success_message(self) -> str:
        """Получить сообщение об успешном сохранении"""
        return self.get_text(self.success_message)

    def clear_form(self):
        """Очистить форму"""
        self.fill(self.contract_input, "")
        # Для очистки поля даты используем специальный подход
        self.date_input.click()
        self.date_input.press('Control+a')
        self.date_input.press('Delete')
        print("✓ Форма очищена")
