import pytest
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.contract_page import ContractPage
from pages.contracts_page import ContractsPage
from pages.login_page import LoginPage


@pytest.mark.usefixtures("vpn_connection")
class TestContract:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_config):
        """Вход в систему"""
        login_page = LoginPage(page)
        login_page.login(test_config)
        assert login_page.is_login_successful(), "Не удалось войти"

        self.contract_page = ContractPage(page)
        self.contract_page.open(test_config)

        self.contract_data = ContractFactory()

    def test_close_button(self):
        """Тест кнопки закрытия формы"""

        self.contract_page.click_close_and_verify()

    def test_delete_manager(self):
        """Тест кнопки удаления менеджера"""

        self.contract_page.select_random_manager()
        self.contract_page.delete_manager()
        assert not self.contract_page.is_manager_present(), "Менеджер не удалён"

    def test_delete_work_type(self):
        """Тест кнопки удаления вида работ"""

        self.contract_page.select_random_work_type()
        self.contract_page.delete_work_type()
        assert not self.contract_page.is_work_type_present(), "Вид работ не удалён"

    def test_create_and_find_contract(self, page: Page, test_pdf_file):
        """Создать договор, найти его в списке и открыть"""

        contract = ContractFactory()

        self.contract_page.fill_form(contract, test_pdf_file)
        self.contract_page.click_save_and_verify()

        # Поиск на странице контрактов
        contracts_page = ContractsPage(page)
        contracts_page.open(self.contract_page.config, ContractsPage.PAGE, contracts_page.search_input)
        contracts_page.search(contract.contract_number)

        assert contracts_page.is_row_found(contract.contract_number), \
            f"Договор {contract.contract_number} не найден в списке"

        # Открываем договор
        contracts_page.open_row(contract.contract_number)

        # Проверяем, что открылась страница договора
        assert "edit" in page.url.lower() or "view" in page.url.lower(), \
            f"Договор не открылся. URL: {page.url}"
