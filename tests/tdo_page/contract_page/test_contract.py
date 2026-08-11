import pytest
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.contracts_page import ContractsPage


@pytest.mark.usefixtures("vpn_connection")
class TestContract:

    def test_close_button(self, contract_page):
        """Тест кнопки закрытия формы"""
        contract_page.click_close_and_verify()

    def test_delete_manager(self, contract_page):
        """Тест кнопки удаления менеджера"""
        contract_page.select_random_manager()
        contract_page.delete_manager()
        assert not contract_page.is_manager_present(), "Менеджер не удалён"

    def test_delete_work_type(self, contract_page):
        """Тест кнопки удаления вида работ"""
        contract_page.select_random_work_type()
        contract_page.delete_work_type()
        assert not contract_page.is_work_type_present(), "Вид работ не удалён"

    def test_create_and_find_contract(self, contract_page, page: Page, test_pdf_file, test_config):
        """Создать договор, найти его в списке и открыть"""
        contract = ContractFactory()

        contract_page.fill_form(contract, test_pdf_file)
        contract_page.click_save_and_verify()

        # Поиск на странице контрактов
        contracts_page = ContractsPage.open_page(page, test_config)
        contracts_page.search(contract.contract_number)

        assert contracts_page.is_row_found(contract.contract_number), \
            f"Договор {contract.contract_number} не найден в списке"

        # Открываем договор
        contracts_page.open_row(contract.contract_number)

        # Проверяем, что открылась страница договора
        assert "edit" in page.url.lower() or "view" in page.url.lower(), \
            f"Договор не открылся. URL: {page.url}"


