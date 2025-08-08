import pytest
from playwright.sync_api import Page, expect

# This test assumes:
# - /login serves a simple form with inputs: name="email" and name="password"
# - /api/register and /api/login work
# - /dashboard serves the dashboard.html which fetches history & summary (using cookie set by login)

@pytest.mark.order(1)
def test_login_then_dashboard(page: Page):
    # Register via API first (if already exists, fine)
    page.request.post("http://127.0.0.1:8000/api/register", data={
        "username": "e2euser",
        "email": "e2e@example.com",
        "password": "pass12345"
    })

    # Visit login page and login via form (this sets auth cookie)
    page.goto("http://127.0.0.1:8000/login")
    page.fill('input[name="email"]', "e2e@example.com")
    page.fill('input[name="password"]', "pass12345")
    page.click('button[type="submit"]')

    # Go to dashboard; it should render stats box and (eventually) history table
    page.goto("http://127.0.0.1:8000/dashboard")
    stats = page.locator("#stats")
    expect(stats).to_be_visible()
