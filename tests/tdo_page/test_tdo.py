import pytest
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.contract_page import TdoPage
from pages.contracts_page import ContractsPage
from pages.login_page import LoginPage


@pytest.mark.usefixtures("vpn_connection")
class TestTdo:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_config):
        """Вход и открытие страницы"""
        login_page = LoginPage(page)
        login_page.login(test_config)
        assert login_page.is_login_successful(), "Не удалось войти"

        self.tdo_page = TdoPage(page)
        self.tdo_page.open(test_config)

    def test_close_button(self, page: Page):
        """Тест кнопки закрытия формы"""
        current_url = page.url

        self.tdo_page.click_close_button()
        self.tdo_page.wait_for_navigation()
        self.tdo_page.wait_for_timeout(1000)

        # Проверяем, что ушли со страницы создания
        assert page.url != current_url, "URL не изменился после закрытия"
        assert "new" not in page.url.lower(), "Всё ещё на странице создания"

    def test_delete_manager(self, page: Page):
        """Тест кнопки удаления менеджера"""
        # Добавляем менеджера
        self.tdo_page.select_random_manager()

        # Удаляем
        self.tdo_page.delete_manager()

        # Проверяем, что менеджер удалён (кнопка удаления исчезла)
        assert not self.tdo_page.is_manager_present(), "Менеджер не удалён"

    def test_delete_work_type(self, page: Page):
        """Тест кнопки удаления вида работ"""
        # Добавляем вид работ
        self.tdo_page.select_random_work_type()

        # Удаляем
        self.tdo_page.delete_work_type()

        # Проверяем, что вид работ удалён
        assert not self.tdo_page.is_work_type_present(), "Вид работ не удалён"

    def test_create_and_find_contract(self, page: Page, test_config, test_pdf_file):
        """Создать договор и найти его в списке"""

        contract = ContractFactory()

        self.tdo_page.fill_form(contract, test_pdf_file)
        self.tdo_page.click_safe_button()
        self.tdo_page.wait_for_navigation()
        self.tdo_page.wait_for_timeout(2000)

        assert self.tdo_page.is_saved(), f"Не удалось сохранить {contract.contract_number}"

        contracts_page = ContractsPage(page)
        contracts_page.open(test_config)
        contracts_page.search_contract(contract.contract_number)

        assert contracts_page.is_contract_found(contract.contract_number), \
            f"Договор {contract.contract_number} не найден в списке"
