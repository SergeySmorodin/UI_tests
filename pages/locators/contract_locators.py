class ContractLocators:
    """Локаторы для страницы создания договора"""

    # === Текстовые поля ===
    DATE_INPUT = "#contract_date"

    # === Селекты ===
    STATUS_SELECT = "select"
    FILE_UPLOAD = "#file-upload-input"

    # === Менеджер ===
    ADD_MANAGER_BUTTON = 'button[title="Добавить менеджера"]'
    DELETE_MANAGER_BUTTON = 'xpath=//h-8[contains(text(), "Менеджеры")]/../..//button[@title="Удалить"]'

    # Менеджер — это кнопка, которая открывает выпадающий список
    MANAGER_DROPDOWN_BUTTON = 'xpath=//h-8[contains(text(), "Менеджеры")]/../..//button[.//span[contains(@class, "truncate")]]'

    # Опции в выпадающем списке менеджеров (это кнопки type="button" в открытом списке)
    MANAGER_DROPDOWN_OPTIONS = 'ul[role="listbox"] button[type="button"], div[role="listbox"] button[type="button"]'

    # === Виды работ ===
    ADD_WORK_TYPE_BUTTON = 'button[title="Добавить вид работ"]'
    DELETE_WORK_TYPE_BUTTON = 'xpath=//h-8[contains(text(), "Виды работ")]/../..//button[@title="Удалить"]'

    # Вид работ — это SELECT!
    WORK_TYPE_SELECT = 'xpath=//h-8[contains(text(), "Виды работ")]/../..//select'

    # === Компания ===
    COMPANY_DROPDOWN_BUTTON = 'button:has-text("Выберите компанию")'
    COMPANY_OPTIONS = 'ul button[type="button"], div[role="listbox"] button[type="button"]'

    @staticmethod
    def company_by_name(name: str) -> tuple[str, dict]:
        return 'button[type="button"]', {"has_text": name}
