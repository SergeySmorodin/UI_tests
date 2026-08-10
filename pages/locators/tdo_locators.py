class TdoLocators:
    """Локаторы для страницы создания договора"""

    # === Текстовые поля ===
    DATE_INPUT = "#contract_date"

    # === Селекты ===
    STATUS_SELECT = "select, combobox"
    FILE_UPLOAD = "input[type='file']"

    # === Менеджер ===
    ADD_MANAGER_BUTTON = 'button[title="Добавить менеджера"]'
    DELETE_MANAGER_BUTTON = 'xpath=//*[contains(text(), "Менеджеры")]/following::button[@title="Удалить"][1]'

    # === Виды работ ===
    ADD_WORK_TYPE_BUTTON = 'button[title="Добавить вид работ"]'
    DELETE_WORK_TYPE_BUTTON = 'xpath=//*[contains(text(), "Виды работ")]/following::button[@title="Удалить"][1]'

    # === Общие локаторы ===
    DROPDOWN_OPTIONS = 'li, [role="option"]'
    COMPANY_BUTTONS = 'button[type="button"]'

    @staticmethod
    def company_by_name(name: str) -> tuple[str, dict]:
        """Параметры для filter локатора компании по имени"""
        return 'button[type="button"]', {"has_text": name}

    @staticmethod
    def section_input(section_name: str) -> str:
        """Локатор для input/combobox в секции (Менеджеры/Виды работ)"""
        return f'text={section_name} >> .. >> input, [role="combobox"]'
