import pytest
from playwright.sync_api import sync_playwright
import os
import base64
import allure

@pytest.fixture(scope='session')
def browser():
    headless = os.getenv('HEADLESS', 'false').lower() == 'true'
    browser_name = os.getenv('BROWSER', 'chromium').lower()
    with sync_playwright() as p:
        if browser_name == 'firefox':
            browser = p.firefox.launch(headless=headless)
        elif browser_name == 'webkit':
            browser = p.webkit.launch(headless=headless)
        else:
            browser = p.chromium.launch(headless=headless)
        yield browser
        browser.close()

@pytest.fixture
def page(browser):
    page = browser.new_page()
    yield page
    page.close()

@pytest.fixture
def context():
    """Fixture to share context between steps in a scenario."""
    return {}


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == 'call' and rep.failed:
        page = item.funcargs.get('page')
        if page:
            temp_path = f"tmp_screenshot_{item.name}.png"
            try:
                page.screenshot(path=temp_path, full_page=True)
                with open(temp_path, "rb") as image_file:
                    allure.attach(image_file.read(), name="screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print(f"Fail to capture screenshot: {e}")
            finally:
                if os.path.exists(temp_path):
                    os.remove(temp_path)
        # Attach log file if available
        log_file = os.getenv('LOG_FILE')
        if log_file and os.path.exists(log_file):
            with open(log_file, 'r', encoding='utf-8') as f:
                log_content = f.read()
            if log_content:
                allure.attach(log_content, name="test.log", attachment_type=allure.attachment_type.TEXT)
