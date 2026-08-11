import random

from playwright.sync_api import Page

from config import VPNConfig
from factories.project_factory import ProjectData
from pages.base_page import BasePage
from pages.locators.project_locators import ProjectLocators


class ProjectPage(BasePage):
    """Страница создания проекта"""

    PAGE = "TDO/Project/new"

    def __init__(self, page: Page):
        super().__init__(page)
        self.loc = ProjectLocators()
        self._init_locators()

    def _init_locators(self):
        self.title = self.page.get_by_text("Создание проекта")
        self.code_input = self.page.locator(self.loc.CODE_INPUT)
        self.start_date_input = self.page.locator(self.loc.START_DATE_INPUT)
        self.code_project_input = self.page.locator(self.loc.CODE_PROJECT_INPUT)
        self.group_select = self.page.locator(self.loc.GROUP_INPUT)
        self.department_select = self.page.locator(self.loc.DEPARTMENT_INPUT)
        self.status_select = self.page.locator(self.loc.STATUS_INPUT)
        self.stop_date_input = self.page.locator(self.loc.STOP_DATE_INPUT)
        self.organisation_input = self.page.locator(self.loc.ORGANISATION_INPUT)
        self.type_project_select = self.page.locator(self.loc.TYPE_PROJECT_INPUT)
        self.kind_project_select = self.page.locator(self.loc.KIND_PROJECT_INPUT)
        self.note_input = self.page.locator(self.loc.NOTE_INPUT)
        self.safe_button = self.page.get_by_role("button", name="Сохранить")
        self.close_button = self.page.get_by_role("button", name="Закрыть")

    def open(self, config: VPNConfig):
        """Открыть страницу создания проекта"""
        super().open(config, self.PAGE, self.title)

    # === Заполнение полей ===

    def fill_code(self, code: str):
        """Заполнить поле Код"""
        self.fill(self.code_input, code)

    def fill_code_project(self, code: str):
        """Заполнить поле Код проекта"""
        self.fill(self.code_project_input, code)

    def fill_organisation(self, organisation: str):
        """Заполнить поле Организация"""
        self.fill(self.organisation_input, organisation)

    def fill_start_date(self, date: str):
        """Заполнить дату начала"""
        self.fill(self.start_date_input, date)

    def fill_stop_date(self, date: str):
        """Заполнить дату окончания"""
        self.fill(self.stop_date_input, date)

    def fill_note(self, note: str):
        self.fill(self.note_input, note)

    # === Заполнение формы из датакласса ===

    def fill_form(self, project: ProjectData):
        """Заполнить все поля формы из объекта ProjectData"""
        self.fill_code(project.code)

        if project.code_project:
            self.fill_code_project(project.code_project)

        if project.organisation:
            self.fill_organisation(project.organisation)

        if project.start_date:
            self.fill_start_date(project.start_date)

        if project.stop_date:
            self.fill_stop_date(project.stop_date)

        if project.note:
            self.fill_note(project.note)

        # Выпадающие списки заполняем только если они не пустые
        # иначе выбираем случайные значения
        self.select_random_status()
        self.select_random_group()
        self.select_random_department()
        self.select_random_type_project()
        self.select_random_kind_project()

    # === Выбор из выпадающих списков ===

    def select_random_status(self):
        """Выбрать случайный статус"""
        self._select_random_option(self.status_select)

    def select_random_group(self):
        """Выбрать случайную группу"""
        self._select_random_option(self.group_select)

    def select_random_department(self):
        """Выбрать случайное подразделение"""
        self._select_random_option(self.department_select)

    def select_random_type_project(self):
        """Выбрать случайный тип проекта"""
        self._select_random_option(self.type_project_select)

    def select_random_kind_project(self):
        """Выбрать случайный вид проекта"""
        self._select_random_option(self.kind_project_select)

    def _select_random_option(self, select_locator):
        """Выбрать случайную опцию из select"""
        # Сначала кликаем по селекту чтобы он открылся
        try:
            select_locator.click()
            self.wait_for_timeout(300)
        except:
            pass

        # Получаем список опций
        options = select_locator.locator('option')
        option_count = options.count()

        if option_count > 1:  # Пропускаем первый пустой option
            # Выбираем случайный индекс начиная с 1
            random_index = random.randint(1, option_count - 1)
            random_value = options.nth(random_index).get_attribute('value')
            if random_value:
                select_locator.select_option(value=random_value)

    # === Получение значений ===

    def get_code_value(self) -> str:
        """Получить значение поля Код"""
        return self.code_input.input_value()

    def get_code_project_value(self) -> str:
        """Получить значение поля Код проекта"""
        return self.code_project_input.input_value()

    def get_organisation_value(self) -> str:
        """Получить значение поля Организация"""
        return self.organisation_input.input_value()

    def get_start_date_value(self) -> str:
        """Получить значение даты начала"""
        return self.start_date_input.input_value()

    def get_stop_date_value(self) -> str:
        """Получить значение даты окончания"""
        return self.stop_date_input.input_value()

    def get_selected_status(self) -> str:
        """Получить выбранный статус"""
        return self.status_select.input_value()

    def get_note_value(self):
        """Получить заполненное примечание"""
        return self.note_input.input_value()
