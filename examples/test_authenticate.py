import re
from time import sleep

from playwright.sync_api import Page, expect, Route, Dialog, BrowserContext


def test_wiki(page: Page):
    page.goto("https://www.wikipedia.org/")
    page.get_by_role("link", name="English").click()
    expect(page.get_by_text("Welcome to Wikipedia")).to_be_visible()


def test_wiki2(page: Page):
    page.goto("https://www.wikipedia.org/")
    page.get_by_role("link", name="Русский").click()
    page.locator('#vector-main-menu-dropdown').click()
    page.get_by_role("link", name="Содержание").click()
    page.locator('#ca-talk').click()
    expect(page.locator('#firstHeading')).to_have_text("Обсуждение Википедии:Содержание")


def test_request(page: Page):
    """Подмена имя пользователя для проверки серверной обработки аутентификации"""

    def change_request(route: Route):
        data = route.request.post_data
        if data:
            data = data.replace('User49726', 'dfvbdfvfdvf')
        # print(data)
        route.continue_(post_data=data)

    page.route(re.compile('profile/authenticate/'), change_request)
    page.goto("https://gymapp.ru/profile/login/")
    page.locator('#email').fill('User49726')
    page.locator('#password').fill('CQaeok')
    page.get_by_role("button", name="Войти").click()
    sleep(5)


def test_response(page: Page):
    def change_response(route: Route):
        response = route.fetch()
        data = response.text()
        data = data.replace('User49726', 'Сергей')
        route.fulfill(response=response, body=data)

    page.route(re.compile('profile/'), change_response)
    page.goto("https://gymapp.ru/profile/login/")
    page.locator('#email').fill('User49726')
    page.locator('#password').fill('CQaeok')
    page.get_by_role("button", name="Войти").click()
    page.get_by_role("link", name="Мой профиль").click()
    sleep(5)






