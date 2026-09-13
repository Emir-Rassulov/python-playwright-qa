import pytest
from pages.login_page import LoginPage
from test_data.credentials import VALID_USERNAME, VALID_PASSWORD



@pytest.fixture
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.goto()
    login_page.login(VALID_USERNAME, VALID_PASSWORD)

    yield page
