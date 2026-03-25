import os
from pytest_bdd import scenarios, given, then
from pages.home_page import HomePage
from utils.logger import get_logger

# Dynamically set log file path based on REPORT_NAME env variable (set in run.sh)
REPORT_NAME = os.getenv("REPORT_NAME")
LOG_FILE = f"reports/{REPORT_NAME}/test.log" if REPORT_NAME else None
logger = get_logger("test_open_website", log_file=LOG_FILE)

scenarios('../features/open_website.feature')

@given('the user is on the TMDB Discover homepage')
def user_on_homepage(page):
    try:
        logger.info("Navigating to TMDB Discover homepage")
        home = HomePage(page)
        home.goto()
        logger.info("Arrived at homepage")
    except Exception as e:
        logger.error(f"Error navigating to homepage: {e}")
        raise

@then('the page title should be "TMDB Discover"')
def check_title(page):
    try:
        title = page.title()
        logger.info(f"Page title is: {title}")
        if title != "Discover":
            logger.warning(f"Expected title 'Discover', but got '{title}'")
        assert title == "Discover"
    except AssertionError as ae:
        logger.error(f"Assertion failed: {ae}")
        raise
    except Exception as e:
        logger.error(f"Error checking page title: {e}")
        raise
