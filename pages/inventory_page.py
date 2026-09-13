from playwright.sync_api import Locator

from pages.base_page import BasePage
from utils.enums import SortOption


class InventoryPage(BasePage):

    def add_product_to_cart(self, product: str) -> None:
        self.page.locator(
            f'[data-test="add-to-cart-{product}"]'
        ).click()

    def get_cart_badge(self) -> Locator:
        return self.page.locator(
            '[data-test="shopping-cart-badge"]'
        )

    def sort_products(self, sort_option: SortOption) -> None:
        self.page.locator(
            '[data-test="product-sort-container"]'
        ).select_option(sort_option.value)

    def get_product_prices(self) -> list[str]:
        return self.page.locator(
            '[data-test="inventory-item-price"]'
        ).all_text_contents()

    def go_to_cart(self) -> None:
        self.page.locator(
            '[data-test="shopping-cart-link"]'
        ).click()