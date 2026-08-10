import pytest
from playwright.sync_api import Page

from factories.project_factory import ProjectFactory
from pages.login_page import LoginPage
from pages.project_page import ProjectPage
from pages.projects_page import ProjectsPage


@pytest.mark.usefixtures("vpn_connection")
class TestProject:

    @pytest.fixture(autouse=True)
    def setup(self, page: Page, test_config):
        """Вход и открытие страницы"""
        login_page = LoginPage(page)
        login_page.login(test_config)
        assert login_page.is_login_successful(), "Не удалось войти"

        self.project_page = ProjectPage(page)
        self.project_page.open(test_config)
        self.project_data = ProjectFactory()

    # === Тесты кнопок ===

    def test_close_button(self):
        """Тест кнопки закрытия формы"""
        self.project_page.click_close_and_verify()

    def test_safe_button_visible(self):
        """Проверка наличия кнопки Сохранить"""
        assert self.project_page.is_element_visible(self.project_page.safe_button), \
            "Кнопка 'Сохранить' не отображается"

    def test_close_button_visible(self):
        """Проверка наличия кнопки Закрыть"""
        assert self.project_page.is_element_visible(self.project_page.close_button), \
            "Кнопка 'Закрыть' не отображается"

    # === Тесты выпадающих списков ===

    def test_select_all_random_dropdowns(self):
        """Тест выбора случайных значений во всех выпадающих списках"""
        self.project_page.select_random_status()
        self.project_page.select_random_group()
        self.project_page.select_random_department()
        self.project_page.select_random_type_project()
        self.project_page.select_random_kind_project()

        # Проверяем что все селекты имеют значения
        assert self.project_page.status_select.input_value(), "Статус не выбран"
        assert self.project_page.group_select.input_value(), "Группа не выбрана"
        assert self.project_page.department_select.input_value(), "Подразделение не выбрано"
        assert self.project_page.type_project_select.input_value(), "Тип проекта не выбран"
        assert self.project_page.kind_project_select.input_value(), "Вид проекта не выбран"

    # === Тесты заполнения ===

    def test_fill_all_fields(self):
        """Тест заполнения всех полей формы"""
        self.project_page.fill_form(self.project_data)

        # Проверяем заполнение
        assert self.project_page.get_code_value() == self.project_data.code, "Код не совпадает"
        assert self.project_page.get_code_project_value() == self.project_data.code_project, "Код проекта не совпадает"
        assert self.project_page.get_organisation_value() == self.project_data.organisation, "Организация не совпадает"
        assert self.project_page.get_start_date_value() == self.project_data.start_date, "Дата начала не совпадает"
        assert self.project_page.get_stop_date_value() == self.project_data.stop_date, "Дата окончания не совпадает"
        assert self.project_page.get_note_value() == self.project_data.note, "Примечание не совпадает"

    def test_create_and_find_project(self, page: Page, test_config):
        """Тест сохранения со всеми заполненными полями"""
        self.project_page.fill_form(self.project_data)
        self.project_page.click_save_and_verify()

        projects_page = ProjectsPage(page)
        projects_page.open(test_config)
        projects_page.search_project(self.project_data.code)

        assert projects_page.is_project_found(self.project_data.code), \
            f"Проект {self.project_data.code} не найден в списке"

    # === Тесты валидации ===

    def test_dates_validation(self):
        """Тест валидации дат (дата окончания раньше даты начала)"""

        self.project_page.fill_form(self.project_data)
        self.project_page.fill_start_date("31.12.2024")
        self.project_page.fill_stop_date("01.01.2024")
        self.project_page.click_safe_button()

        # Даём время на появление ошибки
        self.project_page.wait_for_timeout(500)

        # Проверяем появление ошибки с ожиданием
        assert self.project_page.is_error_message_visible(timeout=3000), \
            "Нет сообщения об ошибке валидации дат"

        # Проверяем текст ошибки
        error_text = self.project_page.get_error_message_text()
        assert error_text, "Текст ошибки пустой"

        # Проверяем что остались на странице
        assert not self.project_page.is_saved(), \
            "Форма сохранилась с некорректными датами"

    def test_empty_code_validation(self):
        """Тест валидации пустого обязательного поля Код"""
        # Заполняем поля кроме кода
        self.project_page.fill_code_project(self.project_data.code_project)
        self.project_page.fill_organisation(self.project_data.organisation)
        self.project_page.fill_start_date(self.project_data.start_date)

        # Пытаемся сохранить
        self.project_page.click_safe_button()
        self.project_page.wait_for_timeout(1000)

        # Проверяем что остались на странице создания
        assert "new" in self.project_page.get_current_url().lower(), \
            "Форма сохранилась без обязательного поля Код"
