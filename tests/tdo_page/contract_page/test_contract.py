import pytest
import allure
from playwright.sync_api import Page

from factories.contract_factory import ContractFactory
from pages.contracts_page import ContractsPage


@pytest.mark.usefixtures("vpn_connection")
@allure.feature("Управление договорами")
class TestContract:

    @allure.story("Форма договора")
    @allure.title("Проверка кнопки закрытия формы")
    @allure.description("Тест проверяет, что форма договора корректно закрывается по кнопке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_button(self, contract_page):
        """Тест кнопки закрытия формы"""
        with allure.step("Кликнуть на кнопку закрытия и проверить результат"):
            contract_page.click_close_and_verify()

    @allure.story("Управление менеджерами")
    @allure.title("Удаление менеджера из договора")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_manager(self, contract_page):
        """Тест кнопки удаления менеджера"""
        with allure.step("Выбрать случайного менеджера"):
            contract_page.select_random_manager()

        with allure.step("Удалить выбранного менеджера"):
            contract_page.delete_manager()

        with allure.step("Проверить, что менеджер удалён"):
            assert not contract_page.is_manager_present(), "Менеджер не удалён"

    @allure.story("Управление видами работ")
    @allure.title("Удаление вида работ из договора")
    @allure.severity(allure.severity_level.NORMAL)
    def test_delete_work_type(self, contract_page):
        """Тест кнопки удаления вида работ"""
        with allure.step("Выбрать случайный вид работ"):
            contract_page.select_random_work_type()

        with allure.step("Удалить выбранный вид работ"):
            contract_page.delete_work_type()

        with allure.step("Проверить, что вид работ удалён"):
            assert not contract_page.is_work_type_present(), "Вид работ не удалён"

    @allure.story("Создание и поиск договора")
    @allure.title("Создание, поиск и открытие договора")
    @allure.description("Полный цикл: создание договора, поиск в списке и открытие")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_and_find_contract(self, contract_page, page: Page, test_pdf_file, test_config):
        """Создать договор, найти его в списке и открыть"""
        with allure.step("Сгенерировать тестовые данные для договора"):
            contract = ContractFactory()
            allure.attach(str(contract.__dict__), "Данные договора", allure.attachment_type.JSON)

        with allure.step("Заполнить форму договора"):
            contract_page.fill_form(contract, test_pdf_file)

        with allure.step("Сохранить договор"):
            contract_page.click_save_and_verify()

        with allure.step(f"Найти договор {contract.contract_number} в списке"):
            contracts_page = ContractsPage.open_page(page, test_config)
            contracts_page.search(contract.contract_number)

        with allure.step(f"Проверить наличие договора {contract.contract_number}"):
            assert contracts_page.is_row_found(contract.contract_number), \
                f"Договор {contract.contract_number} не найден в списке"

        with allure.step("Открыть найденный договор"):
            contracts_page.open_row(contract.contract_number)

        with allure.step("Проверить, что открылась страница договора"):
            assert "edit" in page.url.lower() or "view" in page.url.lower(), \
                f"Договор не открылся. URL: {page.url}"