from pages.navigation_menu import NavigationMenu
from playwright.sync_api import expect

def test_user_can_logout(logged_in_page):
    navigation_menu = NavigationMenu(logged_in_page)
    navigation_menu.open_menu()
    navigation_menu.logout()
    expect(logged_in_page).to_have_url("https://www.saucedemo.com/")