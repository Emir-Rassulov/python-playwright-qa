from pages.base_page import BasePage

class LoginPage(BasePage):


    def goto(self):
        self.page.goto("https://www.saucedemo.com")

    def login(self, username, password):
        self.page.locator("[data-test=username]").fill(username)
        self.page.locator("[data-test=password]").fill(password)
        self.page.locator("[data-test=login-button]").click()