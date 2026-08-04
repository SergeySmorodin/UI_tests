from playwright.sync_api import Page, Dialog


def test_alert(page: Page):
    """Всплывающее окно, нажимаем перед добавлением в корзину"""
    page.goto('https://www.demoblaze.com/')

    def accept_allert(alert: Dialog):
        print(alert.message)
        alert.accept()

    page.on('dialog', accept_allert)
    page.get_by_role("link", name="Samsung galaxy s6").click()
    page.get_by_role("link", name="Add to cart").click()
    page.wait_for_event('dialog')
    page.locator('#cartur').click()
