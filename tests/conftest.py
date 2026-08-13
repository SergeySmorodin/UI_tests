import pytest

from factories.contract_factory import ContractFactory
from factories.project_factory import ProjectFactory
from pages.contract_page import ContractPage
from pages.login_page import LoginPage
from pages.personal_account_page import PersonalAccountPage
from pages.project_page import ProjectPage


@pytest.fixture
def login_page(page):
    """Страница логина (без авторизации)"""
    return LoginPage(page)


@pytest.fixture
def authenticated_page(page, test_config):
    """Авторизованная страница (playwright Page)"""
    login_page = LoginPage(page)
    login_page.login(test_config)
    assert login_page.is_login_successful(), "Не удалось войти"
    return page  # Чистый Page для страниц, которым не нужны методы LoginPage


@pytest.fixture
def authenticated_login_page(page, test_config):
    """Авторизованная страница (LoginPage с методами)"""
    login_page = LoginPage(page)
    login_page.login(test_config)
    assert login_page.is_login_successful(), "Не удалось войти"
    return login_page  # LoginPage с методами для тестов логина


@pytest.fixture
def project_page(authenticated_page, test_config):
    """Страница создания проекта"""
    page = ProjectPage(authenticated_page)
    page.open(test_config)
    return page


@pytest.fixture
def contract_page(authenticated_page, test_config):
    """Страница создания контракта"""
    page = ContractPage(authenticated_page)
    page.open(test_config)
    return page


@pytest.fixture
def personal_account_page(authenticated_page, test_config):
    """Страница личного кабинета"""
    page = PersonalAccountPage(authenticated_page)
    page.open(test_config)
    return page


############################################## Тестовые данные ########################################################
@pytest.fixture
def project_data():
    """Тестовые данные проекта"""
    return ProjectFactory()


@pytest.fixture
def contract_data():
    """Тестовые данные контракта"""
    return ContractFactory()
