from playwright.sync_api import Page, BrowserContext


def test_select_first(page: Page):
    """Найдем первый селектор выпадающего списка sorter и кликнем на элемент Price"""
    page.goto('https://')
    page.locator('#sorter').first.select_option('Price')
