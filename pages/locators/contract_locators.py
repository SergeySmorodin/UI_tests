class ContractLocators:
    """Локаторы для страницы создания договора"""

    # === Текстовые поля ===
    DATE_INPUT = "#contract_date"

    # === Селекты ===
    STATUS_SELECT = "select"
    FILE_UPLOAD = "#file-upload-input"

    # === Менеджер ===
    ADD_MANAGER_BUTTON = 'button[title="Добавить менеджера"]'
    DELETE_MANAGER_BUTTON = 'button[title="Удалить"]'  # Внутри строки менеджера

    # Строка менеджера (div с кнопкой и кнопкой удаления)
    MANAGER_ROW = 'xpath=//h-8[contains(text(), "Менеджеры")]/../..//div[contains(@class, "flex items-center gap-2")]'

    # Кнопка менеджера внутри строки (та, что открывает выпадающий список)
    MANAGER_DROPDOWN_BUTTON = 'xpath=//h-8[contains(text(), "Менеджеры")]/../..//div[contains(@class, "flex items-center gap-2")]//button[.//span[contains(@class, "truncate")]]'

    # === Виды работ ===
    ADD_WORK_TYPE_BUTTON = 'button[title="Добавить вид работ"]'
    DELETE_WORK_TYPE_BUTTON = 'button[title="Удалить"]'  # Внутри строки вида работ

    # Строка вида работ (div с select и кнопкой удаления)
    WORK_TYPE_ROW = 'xpath=//h-8[contains(text(), "Виды работ")]/../..//div[contains(@class, "flex items-center gap-2")]'

    # Select внутри строки вида работ
    WORK_TYPE_SELECT = 'xpath=//h-8[contains(text(), "Виды работ")]/../..//div[contains(@class, "flex items-center gap-2")]//select'

    # === Компания ===
    COMPANY_DROPDOWN_BUTTON = 'button:has-text("Выберите компанию")'
    COMPANY_OPTIONS = 'button[type="button"]'  # Кнопки в выпадающем списке компаний

    @staticmethod
    def company_by_name(name: str) -> tuple[str, dict]:
        return 'button[type="button"]', {"has_text": name}
