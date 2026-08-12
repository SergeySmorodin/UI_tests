import pytest
import allure
from playwright.sync_api import Page

from pages.projects_page import ProjectsPage


@pytest.mark.usefixtures("vpn_connection")
@allure.feature("Управление проектами")
class TestProject:

    # === Тесты кнопок ===

    @allure.story("Форма проекта")
    @allure.title("Проверка кнопки закрытия формы")
    @allure.description("Тест проверяет, что форма проекта корректно закрывается по кнопке")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_close_button(self, project_page):
        """Тест кнопки закрытия формы"""
        with allure.step("Кликнуть на кнопку закрытия и проверить результат"):
            project_page.click_close_and_verify()

    @allure.story("Форма проекта")
    @allure.title("Проверка отображения кнопки 'Сохранить'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_safe_button_visible(self, project_page):
        """Проверка наличия кнопки Сохранить"""
        with allure.step("Проверить видимость кнопки 'Сохранить'"):
            assert project_page.is_element_visible(project_page.safe_button), \
                "Кнопка 'Сохранить' не отображается"

    @allure.story("Форма проекта")
    @allure.title("Проверка отображения кнопки 'Закрыть'")
    @allure.severity(allure.severity_level.NORMAL)
    def test_close_button_visible(self, project_page):
        """Проверка наличия кнопки Закрыть"""
        with allure.step("Проверить видимость кнопки 'Закрыть'"):
            assert project_page.is_element_visible(project_page.close_button), \
                "Кнопка 'Закрыть' не отображается"

    # === Тесты заполнения ===

    @allure.story("Заполнение формы")
    @allure.title("Заполнение всех полей формы без сохранения")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_fill_all_fields(self, project_page, project_data):
        """Тест заполнения всех полей формы без сохранения"""
        with allure.step("Заполнить все поля формы"):
            project_page.fill_form(project_data)

        with allure.step("Проверить корректность заполнения"):
            project_page.verify_form_data(project_data)

    @allure.story("Создание и поиск проекта")
    @allure.title("Создание, поиск и открытие проекта")
    @allure.description("Полный цикл: создание проекта, поиск в списке и открытие")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_create_and_find_project(self, project_page, project_data, page: Page, test_config):
        """Тест сохранения со всеми заполненными полями"""
        with allure.step("Сгенерировать тестовые данные для проекта"):
            allure.attach(str(project_data.__dict__), "Данные проекта", allure.attachment_type.JSON)

        with allure.step("Заполнить форму проекта"):
            project_page.fill_form(project_data)

        with allure.step("Сохранить проект"):
            project_page.click_save_and_verify()

        with allure.step(f"Найти проект {project_data.code} в списке"):
            projects_page = ProjectsPage.open_page(page, test_config)
            projects_page.search(project_data.code)

        with allure.step(f"Проверить наличие проекта {project_data.code}"):
            assert projects_page.is_row_found(project_data.code), \
                f"Проект {project_data.code} не найден в списке"

        with allure.step("Открыть найденный проект"):
            projects_page.open_row(project_data.code)

        with allure.step("Проверить, что открылась страница проекта"):
            assert "edit" in page.url.lower() or "view" in page.url.lower(), \
                f"Проект не открылся. URL: {page.url}"

    # === Тесты валидации ===

    @allure.story("Валидация формы")
    @allure.title("Проверка валидации пустого обязательного поля Код")
    @allure.description("Тест проверяет, что форма не сохраняется без обязательного поля Код")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_empty_code_validation(self, project_page, project_data):
        """Тест валидации пустого обязательного поля Код"""
        with allure.step("Заполнить поля, кроме кода"):
            project_page.fill_code_project(project_data.code_project)
            project_page.fill_organisation(project_data.organisation)
            project_page.fill_start_date(project_data.start_date)

        with allure.step("Нажать кнопку сохранить"):
            project_page.click_safe_button()
            project_page.wait_for_timeout(1000)

        with allure.step("Проверить, что форма не сохранилась"):
            assert "new" in project_page.get_current_url().lower(), \
                "Форма сохранилась без обязательного поля Код"
