from playwright.sync_api import Page

from config import VPNConfig
from pages.base_page import BasePage


class PersonalAccountPage(BasePage):
    """Личный кабинет"""

    PAGE = "lk"

    def __init__(self, page: Page):
        super().__init__(page)
        self._init_locators()

    def _init_locators(self):
        """Инициализация локаторов"""
        self.title = self.page.get_by_text("Общая информация").first
        self.tab_history_projects = self.page.get_by_role("button").filter(has_text="История проектов").first
        # Локаторы для работы с проектами
        self.project_rows = self.page.locator("tr")  # Строки с проектами
        self.advance_report_button = self.page.locator("#btn_advance_new")  # Кнопка "Авансовый отчет"

    def open(self, config: VPNConfig):
        """Открыть страницу личного кабинета"""
        super().open(config, self.PAGE, self.title)

    def is_lk_successful(self) -> bool:
        """Проверить что страница личного кабинета открылась"""

        try:
            self.page.wait_for_url(lambda url: self.PAGE in url.lower(), timeout=5000)
            self.title.is_visible()
            return True
        except:
            error = self.get_error_message()
            if error:
                print(f"Ошибка: {error}")
            return False

    def go_to_history_projects(self):
        """Перейти в раздел истории проектов"""
        self.tab_history_projects.click()
        self.wait_for_timeout(1000)
        # Ждем появления таблицы с проектами
        self.wait_for_element(self.project_rows.first)

    def get_project_count(self) -> int:
        """Получить количество проектов в таблице"""
        # Исключаем заголовок таблицы, если он есть
        rows = self.project_rows
        count = rows.count()
        print(f"Найдено строк: {count}")

        # Выводим содержимое строк для отладки
        for i in range(min(count, 5)):  # Выводим первые 5 строк
            try:
                row_text = rows.nth(i).text_content()
                print(f"Строка {i}: {row_text[:100]}...")  # Первые 100 символов
            except:
                print(f"Строка {i}: не удалось получить текст")

        return count

    def select_project(self, index: int = 0):
        """Выбрать проект по индексу (по умолчанию первый)"""
        projects_count = self.get_project_count()
        if projects_count == 0:
            raise Exception("Нет доступных проектов")

        if index >= projects_count:
            raise Exception(f"Индекс {index} выходит за пределы. Доступно проектов: {projects_count}")

        # Получаем строку проекта
        project_row = self.project_rows.nth(index)

        # Пробуем разные способы клика
        try:
            # Способ 1: Клик по ссылке внутри строки
            link = project_row.locator("a").first
            if link.count() > 0:
                print(f"Найдена ссылка в строке: {link.text_content()}")
                link.click()
            else:
                # Способ 2: Клик по всей строке
                project_row.click()
        except Exception as e:
            print(f"Ошибка при клике по ссылке: {e}")
            # Способ 3: Клик по всей строке
            project_row.click()

        # Ждем загрузки страницы проекта
        self.wait_for_timeout(2000)
        print(f"URL после клика: {self.page.url}")

    def select_random_project(self):
        """Выбрать случайный проект"""
        import random
        projects_count = self.get_project_count()
        if projects_count == 0:
            raise Exception("Нет доступных проектов")

        # Выбираем случайный индекс, начиная с 1 (пропускаем заголовок, если он есть)
        random_index = random.randint(1, projects_count - 1) if projects_count > 1 else 0
        self.select_project(random_index)
        return random_index

    def click_advance_report_button(self):
        """Нажать на кнопку 'Авансовый отчет'"""
        # Проверяем наличие кнопки
        button_count = self.advance_report_button.count()
        print(f"Кнопок 'Авансовый отчет': {button_count}")

        if button_count == 0:
            # Ищем альтернативные локаторы
            print("Кнопка не найдена по ID, ищем альтернативные локаторы...")

            # Альтернативные локаторы
            alternative_locators = [
                self.page.locator("button").filter(has_text="Авансовый отчет"),
                self.page.locator("input[type='button']").filter(has_text="Авансовый отчет"),
                self.page.locator("a").filter(has_text="Авансовый отчет"),
                self.page.locator("[id*='advance']"),
                self.page.locator("[id*='btn_advance']"),
            ]

            for locator in alternative_locators:
                count = locator.count()
                if count > 0:
                    print(f"Найден альтернативный локатор: {locator}")
                    self.advance_report_button = locator.first
                    break

        # Ждем появления кнопки
        self.wait_for_element(self.advance_report_button, timeout=5000)

        # Проверяем, что кнопка видима и активна
        is_visible = self.advance_report_button.is_visible()
        is_enabled = self.advance_report_button.is_enabled()
        print(f"Кнопка видима: {is_visible}, активна: {is_enabled}")

        if not is_visible or not is_enabled:
            raise Exception(f"Кнопка 'Авансовый отчет' не доступна (visible={is_visible}, enabled={is_enabled})")

        # Кликаем по кнопке
        self.advance_report_button.click()
        self.wait_for_timeout(1000)

    def create_advance_report_with_download(self, project_index: int = 0, timeout: int = 30000):
        """
        Создать авансовый отчет с перехватом скачивания

        Args:
            project_index: Индекс проекта
            timeout: Таймаут ожидания скачивания в миллисекундах

        Returns:
            Download: Объект скачивания
        """
        # Выбираем проект
        self.select_project(project_index)

        # Нажимаем кнопку и ждем скачивание
        try:
            # Используем увеличенный таймаут
            with self.page.expect_download(timeout=timeout) as download_info:
                self.click_advance_report_button()

            download = download_info.value
            filename = download.suggested_filename
            print(f"✓ Файл скачан: {filename}")

            # Проверяем расширение файла
            if not filename.lower().endswith(('.xlsx', '.xls')):
                print(f"⚠ Внимание: файл {filename} не является Excel файлом")

            return download

        except Exception as e:
            print(f"✗ Ошибка при скачивании: {e}")
            # Проверяем, не появилось ли сообщение об ошибке
            error_text = self.get_error_message()
            if error_text:
                print(f"Сообщение об ошибке: {error_text}")

            # Делаем скриншот для отладки
            self.page.screenshot(path="error_screenshot.png")
            print("Скриншот сохранен: error_screenshot.png")

            raise
