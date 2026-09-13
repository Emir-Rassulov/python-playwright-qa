from pages.base_page import BasePage

class CartPage(BasePage):
    def click_checkout(self):
        self.page.locator('[data-test="checkout"]').click()