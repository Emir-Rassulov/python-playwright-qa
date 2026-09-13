# Python + Playwright QA Automation Framework

A test automation framework built with **Python**, **pytest**, and **Playwright**, demonstrating Page Object Model architecture, fixture-based test design, and both UI and API test coverage.

Built as a hands-on learning project to develop production-style QA automation skills — every architectural decision (Page Object structure, fixture scope, test data separation, parametrization) was deliberately reasoned through rather than templated.

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12+ | Core language |
| pytest | Test runner |
| pytest-playwright | Browser automation integration |
| Playwright (sync API) | UI automation engine |
| requests | API test client |
| python-dotenv | Environment variable management |

---

## What This Project Tests

**UI Testing** — [SauceDemo](https://www.saucedemo.com), a demo e-commerce site
- Login: valid credentials, locked-out user, invalid password
- Product inventory: add to cart, cart badge count, price sorting
- Checkout: full happy-path flow, parametrized negative validation (missing first name / last name / postal code)
- Logout / navigation menu

**API Testing** — [DummyJSON](https://dummyjson.com), a public REST API
- Full CRUD coverage: GET, POST, PUT, DELETE
- Positive and negative cases, including parametrized invalid-ID handling (nonexistent ID, zero, negative, non-numeric)

---

## Architecture

```
python-playwright-qa/
├── pages/                  # Page Object Model
│   ├── base_page.py        # Shared constructor (self.page)
│   ├── login_page.py
│   ├── inventory_page.py
│   ├── cart_page.py
│   ├── checkout_page.py
│   └── navigation_menu.py  # Cross-page component (hamburger menu / logout)
│
├── test_data/
│   ├── credentials.py      # Single source of truth for test login data
│   └── api_config.py       # API base URL configuration
│
├── tests/
│   ├── test_saucedemo_login.py
│   ├── test_saucedemo_checkout.py
│   ├── test_saucedemo_logout.py
│   ├── test_saucedemo_smoke.py
│   └── api/
│       └── test_users_api.py
│
├── utils/
│   ├── decorators.py        # @log_execution_time, step() context manager
│   └── enums.py             # SortOption enum
│
├── conftest.py               # Shared fixtures (e.g. logged_in_page)
├── pytest.ini
├── requirements.txt
├── .env.example
└── README.md
```

### Design Principles Applied

- **Page Object Model** with a shared `BasePage`, avoiding duplicated constructor logic across page classes.
- **Fixtures over repetition** — a `logged_in_page` fixture (function-scoped, chosen deliberately for test isolation over raw speed) eliminates repeated login steps across every test that needs an authenticated session.
- **Single source of truth for test data** — credentials and API config live in `test_data/`, not duplicated across test files.
- **Parametrization over duplication** — e.g. one test function covers three checkout validation scenarios (missing first name / last name / postal code) instead of three near-identical functions.
- **Enums over magic strings** — sort options are a `SortOption` enum rather than raw strings, catching invalid values before runtime.
- **Type hints** applied honestly (e.g. `Optional[...]` only where a value can genuinely be absent) to make method contracts clear.
- **No premature abstraction** — e.g. API tests use a plain `BASE_URL` constant rather than a full API client class, since the current scope doesn't yet justify that complexity.

---

## Getting Started

### Prerequisites
- Python 3.12 or newer
- pip

### Installation

```bash
# Clone the repository
git clone https://github.com/Emir-Rassulov/python-playwright-qa.git
cd python-playwright-qa

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows

# Install dependencies
pip install -r requirements.txt

# Install Playwright browser binaries
playwright install
```

### Environment Configuration

Copy the example environment file and adjust values as needed:

```bash
cp .env.example .env
```

---

## Running Tests

```bash
# Run the full suite
pytest

# Run with a visible browser (headed mode)
pytest --headed

# Run a specific test file
pytest tests/test_saucedemo_checkout.py

# Run a specific test function
pytest tests/test_saucedemo_checkout.py::test_checkout_process

# Run tests matching a keyword
pytest -k "checkout"

# Run only the API test suite
pytest tests/api/

# Verbose output (shows each parametrized case individually)
pytest -v
```

### Debugging with Playwright Trace Viewer

```bash
# Run with tracing enabled
pytest --tracing on --output=trace-results

# Open a specific trace
playwright show-trace trace-results/<test-folder-name>/trace.zip
```

---

## Test Coverage Summary

| Area | Coverage |
|---|---|
| UI — Login | Valid login, locked-out user, invalid password |
| UI — Inventory | Add to cart, cart badge, price sorting |
| UI — Checkout | Full flow, parametrized field-validation negatives |
| UI — Navigation | Logout |
| API — Users | Full CRUD (GET, POST, PUT, DELETE), parametrized invalid-ID handling |

---

## Known Limitations

- Login currently drives the real UI form on every test rather than reusing a saved authentication state (`storage_state`) — a deliberate early-stage tradeoff favoring test isolation over speed, revisited if the suite grows significantly.
- No API client abstraction yet — introduced only once request complexity (auth headers, retries) justifies it.
- CI/CD pipeline integration is in progress.

## Planned Improvements

- GitLab CI/CD pipeline: automated test execution, HTML report generation, and artifact storage (traces/screenshots) on every push.
- Expanded API test coverage.
- HTML/Allure reporting for local runs.

---

## Author

Built by Emir Rassulov as part of a structured, self-directed Python + Playwright QA automation learning path.
