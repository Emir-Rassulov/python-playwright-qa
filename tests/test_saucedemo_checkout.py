import pytest
from playwright.sync_api import expect
from pages.checkout_page import CheckoutPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage
from utils.decorators import log_execution_time, step

@log_execution_time
def test_checkout_process(logged_in_page):
    inventory_page = InventoryPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    

    inventory_page.add_product_to_cart("sauce-labs-backpack")

    inventory_page.go_to_cart()

    cart_page.click_checkout()

    with step("Filling checkout form"):
        checkout_page.fill_first_name("John")
        checkout_page.fill_last_name("Doe")
        checkout_page.fill_postal_code("19000")

    checkout_page.click_continue()
    checkout_page.click_finish()

    confirmation_header = checkout_page.get_confirmation_header()

    expect(confirmation_header).to_be_visible()
    expect(confirmation_header).to_contain_text("Thank you")

@pytest.mark.parametrize(
        "first_name, last_name, postal_code, expected_error",
    [
        ("", "Doe", "19000", "First Name is required"),
        ("John", "", "19000", "Last Name is required"),
        ("John", "Doe", "", "Postal Code is required"),
    ],
)

def test_checkout_requires_required_field(logged_in_page, first_name, last_name, postal_code, expected_error):
    inventory_page = InventoryPage(logged_in_page)
    cart_page = CartPage(logged_in_page)
    checkout_page = CheckoutPage(logged_in_page)

    inventory_page.add_product_to_cart("sauce-labs-backpack")
    inventory_page.go_to_cart()
    cart_page.click_checkout()

    if first_name:
        checkout_page.fill_first_name(first_name)
    if last_name:
        checkout_page.fill_last_name(last_name)
    if postal_code:
        checkout_page.fill_postal_code(postal_code)

    checkout_page.click_continue()

    error_message = logged_in_page.locator("[data-test=error]")
    expect(error_message).to_be_visible()
    expect(error_message).to_contain_text(expected_error)





    