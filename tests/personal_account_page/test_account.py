import allure
import pytest


@pytest.mark.usefixtures("vpn_connection")
@allure.feature("Вход в личный кабинет")
class TestPersonalAccountPage:

    @allure.story("Успешный вход")
    @allure.title("Проверка перехода в личный кабинет")
    @allure.description("Тест проверяет успешный вход в личный кабинет")
    @allure.severity(allure.severity_level.NORMAL)
    def test_lk_successful(self, personal_account_page):
        """Тест входа в личный кабинет"""
        page = personal_account_page

        with allure.step("Открыть страницу личного кабинета"):
            assert page.is_lk_successful()

    @allure.story("Работа с проектами")
    @allure.title("Формирование авансового отчета")
    @allure.description("Тест проверяет формирование авансового отчета с выгрузкой Excel")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_create_advance_report(self, personal_account_page):
        """Тест формирования авансового отчета"""
        page = personal_account_page

        with allure.step("Перейти в историю проектов"):
            page.go_to_history_projects()
            projects_count = page.get_project_count()
            allure.attach(f"Количество проектов: {projects_count}", "Информация", allure.attachment_type.TEXT)
            assert projects_count > 0, "Нет доступных проектов"

            # Отладочная информация
            print(f"Найдено проектов: {projects_count}")

        with allure.step("Выбрать проект"):
            # Выбираем первый проект
            selected_index = 0
            if projects_count > 1:
                # Выбираем случайный проект, если их больше одного
                selected_index = page.select_random_project()
                allure.attach(f"Выбран проект с индексом: {selected_index}", "Информация", allure.attachment_type.TEXT)
                print(f"Выбран проект с индексом: {selected_index}")
            else:
                page.select_project(0)
                print("Выбран единственный проект")

            # Отладочная информация
            page.debug_page_state()

        # with allure.step("Сформировать авансовый отчет"):
        #     try:
        #         download = page.create_advance_report_with_download(selected_index)
        #         print(f"Скачивание успешно: {download.suggested_filename}")
        #
        #         # Сохраняем файл
        #         os.makedirs("downloads", exist_ok=True)
        #         download.save_as(f"downloads/{download.suggested_filename}")
        #         print(f"Файл сохранен: downloads/{download.suggested_filename}")
        #
        #     except Exception as e:
        #         # Делаем скриншот для отладки
        #         page.page.screenshot(path="test_error_screenshot.png")
        #         allure.attach.file("test_error_screenshot.png", "Скриншот ошибки", allure.attachment_type.PNG)
        #
        #         raise

    def test_with_debug_artifacts(self, personal_account_page):
        """Тест с сохранением отладочных артефактов"""
        page = personal_account_page

        # Переходим к проектам
        page.go_to_history_projects()
        page.select_project(1)

        # Сохраняем HTML контент
        page.save_page_content("project_page", pretty_print=True)

        # Делаем скриншот
        page.take_screenshot("project_screenshot")

        # Выводим отладочную информацию
        page.debug_info(save_html=True, save_screenshot=True)

        # Или сохраняем все артефакты сразу
        artifacts = page.save_debug_artifacts("before_click")

        # Кликаем на кнопку
        page.click_advance_report_button()

        # Сохраняем артефакты после клика
        artifacts_after = page.save_debug_artifacts("after_click")
