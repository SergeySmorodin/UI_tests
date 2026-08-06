import pytest
from playwright.sync_api import Page

from pages.login_page import LoginPage
from pages.tdo_page import TdoPage


@pytest.mark.usefixtures("vpn_connection")
class TestTdoPage:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_config):
        """Предварительный вход в систему перед каждым тестом"""
        login_page = LoginPage(page)
        login_page.login(test_config)
        assert login_page.is_login_successful(), "Не удалось войти в систему"

    def test_create_contract_successfully(self, page: Page, test_config):
        """Тест успешного создания договора"""
        tdo_page = TdoPage(page)

        # Открываем страницу создания договора
        tdo_page.open(test_config)

        # Проверяем, что форма отображается
        assert tdo_page.check_tdo_form_visible(), "Форма не загружена"
        print("✓ Форма создания договора отображается")

        # Заполняем и сохраняем
        contract_number, contract_date = tdo_page.save_contract()

        # Проверяем результат
        assert tdo_page.is_contract_saved(), \
            f"Договор не сохранен. Текущий URL: {page.url}"
        print(f"✓ Договор {contract_number} от {contract_date} успешно создан")

    def test_form_validation_empty_fields(self, page: Page, test_config):
        """Тест валидации - пустые поля"""
        tdo_page = TdoPage(page)
        tdo_page.open(test_config)

        # Нажимаем сохранить без заполнения полей
        tdo_page.click_safe_button()
        tdo_page.wait_for_navigation()
        tdo_page.wait_for_timeout(2000)

        # Проверяем, что договор не создан
        assert not tdo_page.is_contract_saved(), \
            "Договор не должен быть создан с пустыми полями"

        # Проверяем сообщение об ошибке или что остались на странице
        error_message = tdo_page.get_error_message()
        if error_message:
            print(f"✓ Получено сообщение об ошибке: {error_message}")
        else:
            print("✓ Договор не создан (остались на странице создания)")

    def test_create_multiple_contracts(self, page: Page, test_config):
        """Тест создания нескольких договоров подряд"""
        tdo_page = TdoPage(page)

        contracts = []
        for i in range(3):
            tdo_page.open(test_config)
            contract_number = f"TEST-MULTI-{i + 1}"
            contract_date = f"{i + 1:02d}.01.2024"

            tdo_page.save_contract(contract_number, contract_date)

            assert tdo_page.is_contract_saved(), \
                f"Договор {contract_number} не сохранен"
            contracts.append((contract_number, contract_date))
            print(f"✓ Создан договор {i + 1}/3: {contract_number}")

        print(f"✓ Создано {len(contracts)} договоров")

    def test_clear_form(self, page: Page, test_config):
        """Тест очистки формы"""
        tdo_page = TdoPage(page)
        tdo_page.open(test_config)

        # Заполняем форму
        tdo_page.fill_contract_form("TEST-CLEAR", "01.01.2024")

        # Очищаем
        tdo_page.clear_form()

        # Проверяем, что поля пустые
        contract_value = tdo_page.contract_input.input_value()
        date_value = tdo_page.date_input.input_value()

        assert contract_value == "", f"Поле договора не очищено: {contract_value}"
        assert date_value == "", f"Поле даты не очищено: {date_value}"
        print("✓ Форма успешно очищена")
