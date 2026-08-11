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

    # === Тесты заполнения ===

    def test_fill_all_fields(self, project_page, project_data):
        """Тест заполнения всех полей формы без сохранения"""
        project_page.fill_form(project_data)

        # Проверяем заполнение
        project_page.verify_form_data(project_data)

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
