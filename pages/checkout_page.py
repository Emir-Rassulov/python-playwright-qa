from pages.base_page import BasePage

class CheckoutPage(BasePage):

    def fill_first_name(self, first_name):
        self.page.locator('[data-test="firstName"]').fill(first_name)

    def fill_last_name(self, last_name):
        self.page.locator('[data-test="lastName"]').fill(last_name)

    def fill_postal_code(self, postal_code):
        self.page.locator('[data-test="postalCode"]').fill(postal_code)

    def click_continue(self):
        self.page.locator('[data-test="continue"]').click()

    def click_finish(self):
        self.page.locator('[data-test="finish"]').click()

    def get_confirmation_header(self):
        return self.page.locator('[data-test="complete-header"]')

    