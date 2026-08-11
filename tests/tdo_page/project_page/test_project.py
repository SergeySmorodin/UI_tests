import pytest
from playwright.sync_api import Page

from pages.projects_page import ProjectsPage


@pytest.mark.usefixtures("vpn_connection")
class TestProject:

    # === Тесты кнопок ===

    def test_close_button(self, project_page):
        """Тест кнопки закрытия формы"""
        project_page.click_close_and_verify()

    def test_safe_button_visible(self, project_page):
        """Проверка наличия кнопки Сохранить"""
        assert project_page.is_element_visible(project_page.safe_button), \
            "Кнопка 'Сохранить' не отображается"

    def test_close_button_visible(self, project_page):
        """Проверка наличия кнопки Закрыть"""
        assert project_page.is_element_visible(project_page.close_button), \
            "Кнопка 'Закрыть' не отображается"

    # === Тесты выпадающих списков ===

    def test_select_all_random_dropdowns(self, project_page):
        """Тест выбора случайных значений во всех выпадающих списках"""
        project_page.select_random_status()
        project_page.select_random_group()
        project_page.select_random_department()
        project_page.select_random_type_project()
        project_page.select_random_kind_project()

        # Проверяем что все селекты имеют значения
        assert project_page.status_select.input_value(), "Статус не выбран"
        assert project_page.group_select.input_value(), "Группа не выбрана"
        assert project_page.department_select.input_value(), "Подразделение не выбрано"
        assert project_page.type_project_select.input_value(), "Тип проекта не выбран"
        assert project_page.kind_project_select.input_value(), "Вид проекта не выбран"

    # === Тесты заполнения ===

    def test_fill_all_fields(self, project_page, project_data):
        """Тест заполнения всех полей формы"""
        project_page.fill_form(project_data)

        # Проверяем заполнение
        assert project_page.get_code_value() == project_data.code, "Код не совпадает"
        assert project_page.get_code_project_value() == project_data.code_project, "Код проекта не совпадает"
        assert project_page.get_organisation_value() == project_data.organisation, "Организация не совпадает"
        assert project_page.get_start_date_value() == project_data.start_date, "Дата начала не совпадает"
        assert project_page.get_stop_date_value() == project_data.stop_date, "Дата окончания не совпадает"
        assert project_page.get_note_value() == project_data.note, "Примечание не совпадает"

    def test_create_and_find_project(self, project_page, project_data, page: Page, test_config):
        """Тест сохранения со всеми заполненными полями"""
        project_page.fill_form(project_data)
        project_page.click_save_and_verify()

        projects_page = ProjectsPage.open_page(page, test_config)
        projects_page.search(project_data.code)

        assert projects_page.is_row_found(project_data.code), \
            f"Проект {project_data.code} не найден в списке"

        # Открываем проект
        projects_page.open_row(project_data.code)

        # Проверяем, что открылась страница проекта
        assert "edit" in page.url.lower() or "view" in page.url.lower(), \
            f"Проект не открылся. URL: {page.url}"

    # === Тесты валидации ===

    def test_empty_code_validation(self, project_page, project_data):
        """Тест валидации пустого обязательного поля Код"""
        # Заполняем поля кроме кода
        project_page.fill_code_project(project_data.code_project)
        project_page.fill_organisation(project_data.organisation)
        project_page.fill_start_date(project_data.start_date)

        # Пытаемся сохранить
        project_page.click_safe_button()
        project_page.wait_for_timeout(1000)

        # Проверяем что остались на странице создания
        assert "new" in project_page.get_current_url().lower(), \
            "Форма сохранилась без обязательного поля Код"
