from pages.base_page import BasePage

class NavigationMenu(BasePage):
   
    def open_menu(self):
            self.page.get_by_role("button", name="Open Menu").click()

    def logout(self):
         self.page.locator('[data-test="logout-sidebar-link"]').click()