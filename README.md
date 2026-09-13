# Alza.cz QA Automation Portfolio

An end-to-end test automation suite built with **Playwright + TypeScript**, targeting the live production e-commerce site [alza.cz](https://www.alza.cz). This project was built as a portfolio piece to demonstrate practical QA automation skills against a real, unmodified, hostile-to-bots production system — not a sandboxed demo site.

## Why a live production site, not a demo/sandbox

Most learning resources use purpose-built demo sites (predictable markup, no anti-bot protection, no real-world flakiness). This project deliberately targets a real site instead, to demonstrate skills that only show up against production systems: diagnosing genuine application bugs, reverse-engineering unstable markup, distinguishing real defects from environmental noise, and working around (not defeating) real anti-bot infrastructure.

This tradeoff is documented honestly throughout this README — several tests and CI runs are affected by things outside this suite's control (see **Known Issues** below), and that's treated as a feature of the project, not a flaw to hide.

## Tech stack

- **Playwright** (TypeScript) — test runner and browser automation
- **Page Object Model** architecture, with a shared `BasePage` for common navigation/setup logic
- **Custom fixtures** for generic test infrastructure (e.g., blocking third-party overlays)
- **ESLint + Prettier**, with `eslint-plugin-playwright` for framework-specific linting
- **GitHub Actions** for CI (see [CI/CD](#cicd) below for important caveats)

## Project structure

```
alza-qa-portfolio/
├── .github/workflows/         # CI workflow (manual-trigger only, see below)
├── components/
│   └── CookieBanner.ts        # Cookie-consent dismissal, used by BasePage
├── fixtures/
│   └── testFixtures.ts        # Generic test setup (third-party overlay blocking)
├── pages/                     # Page Object classes
│   ├── BasePage.ts            # Shared navigation + cookie dismissal
│   ├── HomePage.ts
│   ├── SearchResultsPage.ts
│   ├── CategoryPage.ts
│   ├── ProductPage.ts
│   ├── CartPage.ts
│   └── CheckoutPage.ts
├── test-data/                 # Centralized test data (see "Test data" below)
├── utils/
│   └── hydrationRetry.ts      # Shared retry helpers for a recurring site bug
├── tests/e2e/
│   └── search.spec.ts         # All 22 tests
├── .eslintrc.json / eslint.config.js
├── .prettierrc.json
└── playwright.config.ts
```

## Test coverage

~22 tests across 6 functional areas:

| Block | Area | Tests |
|---|---|---|
| 1 | Search | 6 (happy path, no-results, autocomplete, empty query ×2, XSS smoke test) |
| 2 | Catalog / filters | 5 (category navigation, price filter, sort, pagination, filter+sort combined) |
| 3 | Product page | 4 (required elements, search→product consistency, two distinct "unavailable product" UI patterns) |
| 4 | Cart | 4 (add to cart, quantity → total recalculation, item removal, multi-item total) |
| 5 | Checkout | 1 (delivery + payment selection, intentionally stops short of a real purchase) |
| 6 | API | 2 (search-suggestion endpoint, WAF behavior on suspicious input) |

**Safety principle followed throughout:** no test completes a real purchase. Checkout tests stop after delivery/payment selection, never submitting final order confirmation.

## Architecture notes

- **`BasePage`** centralizes navigation (`goto()`), which automatically handles cookie-consent dismissal via `CookieBanner` — individual page objects and tests never need to think about this.
- **Fixtures** (`fixtures/testFixtures.ts`) are kept intentionally generic (currently: blocking the Google "One Tap" sign-in iframe from intercepting clicks) — site-specific UI knowledge lives in page objects/components, not in fixture setup.
- **`utils/hydrationRetry.ts`** provides two shared helpers addressing the recurring hydration bug (see Known Issues #1) from its two distinct symptoms, rather than duplicating retry logic per page object:
  - `waitWithHydrationRetry(page, locator)` — for content that fails to render (reloads once if the expected element never appears).
  - `retryActionOnHydrationFailure(page, action, waitForSuccess)` — for actions that register but silently fail to produce their expected effect (e.g. a click that doesn't navigate); retries the action itself across reloads, up to a max attempt count.

### Test data

All test data lives in `test-data/`, separated from test logic:

| File | Contents |
|---|---|
| `products.ts` | Product URLs used across tests (e.g. the iPhone 17 used throughout cart/checkout flows, a known out-of-stock item, a product that triggers a server-side checkout failure) |
| `categories.ts` | Category navigation targets (menu label, expected URL pattern, expected heading) |
| `priceFilters.ts` | Min/max price ranges used in filter tests |
| `searchTerms.ts` | Search query strings, including a dynamically-generated (timestamped) "non-existent product" term to avoid relying on a single static string across repeated runs |
| `testCustomer.ts` | Checkout test data (postcode, delivery district) |
| `xssPayloads.ts` / `xssGenerator.ts` | The XSS smoke-test payload template and its generator (see Known Issues #6) |

This keeps page objects and tests free of embedded magic strings/URLs, and means updating a product URL or test value only requires a change in one place.

## Running locally

```bash
npm install
npx playwright install
npm run lint          # ESLint
npm run format:check  # Prettier check
npx playwright test tests/e2e/search.spec.ts --project=firefox
```

**Firefox is the recommended browser for running this suite** — see Known Issues #4 for why Chromium and WebKit are unreliable against this specific site.

## CI/CD

A GitHub Actions workflow (`.github/workflows/playwright.yml`) is included and demonstrates a working CI pipeline (checkout, dependency install, browser install, test execution, artifact upload). **However:**

**This workflow is manually triggered only (`workflow_dispatch`), and its pass/fail result is not representative of the suite's actual correctness.** GitHub-hosted runners use well-known datacenter IP ranges (Azure/AWS), which Alza's Cloudflare bot protection reliably serves a Turnstile "prove you're human" challenge page to, instead of the real site. In a test run from a GitHub-hosted runner, 20 of 21 executed tests failed — not due to application bugs or test defects, but because the runner never saw real page content, only Cloudflare's challenge page.

This is confirmed, not speculative: trace screenshots from that run show the literal Cloudflare interstitial ("Prosím, potvrďte, že jste z masa a kostí" — "Please confirm you're made of flesh and bone"), and the failure pattern (near-total failure, uniform timeout shape, ~15s per test) is consistent with every request being blocked at the same point, rather than isolated application issues.

**This CI workflow exists to demonstrate pipeline configuration and reporting capability — the meaningful evidence of this suite's behavior comes from local runs**, which use a residential IP not subject to the same bot-detection treatment.

Realistic paths to a genuinely green CI run (not implemented, out of scope for this project):
- A self-hosted runner on a non-datacenter IP (e.g., a home machine registered as a GitHub Actions runner)
- Scheduling runs at low frequency from a residential/ISP proxy (adds cost/complexity, and arguably undermines the point of testing against real anti-bot protection)

## Known Issues

These are genuine, reproduced findings about the live site's behavior — not defects in this test suite. Each was diagnosed through direct evidence (trace screenshots, console logs, network inspection), not assumption.

### 1. React hydration failures (Minified React error #421/#418/#423)

Alza's React application intermittently fails to complete hydration, leaving parts of a page (typically everything below the header/heading) stuck in a skeleton-loading state, while the rest of the page appears normal. Confirmed via browser console errors on multiple, unrelated page types:
- Cart page (`Order1.htm`)
- Checkout delivery/payment page (`Order2.htm` transition)
- Category listing pages (product grid failing to render)

**Mitigation:** two shared helpers in `utils/hydrationRetry.ts` address this from its two distinct symptoms — content that never renders (`waitWithHydrationRetry`), and actions that register but silently fail to produce their expected effect, such as a "Continue" click that doesn't navigate (`retryActionOnHydrationFailure`). Both reload the page and retry once the expected condition still hasn't been met. This resolves most occurrences but not all — occasional residual flakiness remains and is treated as expected variance on a live, uncontrolled system.

### 2. Two distinct "unavailable product" UI patterns

Out-of-stock products on Alza do not behave consistently:
- **Pattern A:** the "Add to cart" button is hidden entirely; a "Hlídat dostupnost" ("Watch availability") link is shown instead.
- **Pattern B:** the "Add to cart" button remains visible and clickable, but attempting to complete the add produces a "Vložení do košíku se nezdařilo" ("Adding to cart failed") error after a discount-decline confirmation step.

Both are covered by separate tests, since collapsing them into one assumption would have missed real coverage of one of the two patterns.

### 3. Cloudflare blocks Playwright's bare API request fixture

Direct `request.get()` calls (Playwright's `APIRequestContext`, used without a real browser context) to `webapi.alza.cz` are blocked with a `403`, regardless of query content — confirmed by testing identical requests via `page.goto()` (passes) vs. the bare `request` fixture (fails universally, even for entirely benign search terms). This indicates Cloudflare requires browser-level TLS/JS fingerprinting signals that a headless API-only request cannot provide. All API tests in this suite are implemented via `page.goto()` for this reason, not the `request` fixture.

### 4. Chromium and WebKit are unreliable against this site; Firefox is not

Cross-browser testing revealed asymmetric bot-detection behavior:
- **Chromium:** reliably served a Cloudflare Turnstile challenge page instead of the real site — appears to be fingerprinted via CDP (Chrome DevTools Protocol) artifacts specific to how Playwright drives Chromium.
- **WebKit:** inconsistent silent throttling/timeouts, without a visible challenge page.
- **Firefox:** reliably passes; not flagged by the same heuristics.

**Firefox is used as the primary/only browser for this suite as a result** — this is a deliberate engineering decision based on evidence, not a limitation of the test code.

### 5. CI runs from shared/datacenter IPs are blocked outright

See the [CI/CD](#cicd) section above — this is the most significant limitation affecting this project, and the reason CI is manual-trigger-only rather than running on every push.

### 6. Reflected-XSS smoke test is basic-scope by design

A single-vector reflected-XSS test exists on the search input, as a defense-in-depth smoke check — not a substitute for a dedicated penetration test or security audit. It intentionally covers one input field and one payload shape; a comprehensive security review would need broader scope (multiple injection contexts, stored-XSS testing, additional input surfaces) that falls outside standard QA automation responsibility.

---

*Built as a self-directed learning project to practice production-grade Playwright automation, from first principles (variables, loops, functions) through architecture (POM, fixtures, CI) and real-world debugging against a live, actively-defended production system.*
