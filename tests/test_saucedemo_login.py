# SauceDemo's known test credentials (public, documented on their login page)
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from playwright.sync_api import expect
from test_data.credentials import (
    VALID_USERNAME,
    VALID_PASSWORD,
    LOCKED_USERNAME,
    INVALID_PASSWORD,
)
from utils.enums import SortOption


def test_valid_credentials_are_defined_correctly():
    assert VALID_USERNAME == "standard_user"
    assert VALID_PASSWORD == "secret_sauce"


def test_locked_user_is_different_from_valid_user():
    assert LOCKED_USERNAME != VALID_USERNAME

def test_invalid_password_is_different_from_valid_password():
    assert INVALID_PASSWORD != VALID_PASSWORD

def test_valid_login_redirects_to_inventory_page(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)
    expect(page).to_have_url("https://www.saucedemo.com/inventory.html")

def test_locked_user_login_shows_error_message(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(LOCKED_USERNAME, VALID_PASSWORD)
    error_message = page.locator("[data-test=error]")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text("Epic sadface: Sorry, this user has been locked out.")


def test_add_product_shows_cart_badge(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)

    inventory_page.add_product_to_cart("sauce-labs-backpack")

    cart_badge = inventory_page.get_cart_badge()

    expect(cart_badge).to_be_visible()
    expect(cart_badge).to_have_text("1")

def test_sort_products_by_price_low_to_high(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)

    inventory_page.sort_products(SortOption.PRICE_LOW_TO_HIGH)

    prices = inventory_page.get_product_prices()

    prices = [float(price.replace("$", "")) for price in prices]

    assert prices == sorted(prices)

    




