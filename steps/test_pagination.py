import os
from pytest_bdd import scenarios, given, when, then, parsers
from pages.home_page import HomePage
from pages.common_page import CommonPage
from utils.logger import get_logger

REPORT_NAME = os.getenv("REPORT_NAME")
LOG_FILE = f"reports/{REPORT_NAME}/test.log" if REPORT_NAME else None
logger = get_logger("test_pagination", log_file=LOG_FILE)

scenarios('../features/pagination.feature')

@given('the user opens the TMDB Discover website')
def open_tmdb_home(page):
    logger.info("Opening TMDB Discover website")
    home = HomePage(page)
    home.goto()

@given(parsers.parse('the user is on the "{category}" category page'))
def on_category(page, category):
    logger.info(f"Navigating to category: {category}")
    # Implement navigation to the category if needed
    # Example: page.click(f'button[aria-label="{category}"]')

@given('the user notes the title of the first movie on the current page')
def note_first_movie_title(page, context={}):
    logger.info("Noting the first movie title on the current page")
    common = CommonPage(page)
    first_title = common.get_first_movie_title()
    context['first_title'] = first_title
    logger.info(f"First movie title: {first_title}")

@when('the user clicks the "Next" button')
def click_next(page):
    logger.info("Clicking the Next button")
    common = CommonPage(page)
    common.click_next()

@when('the user scroll to pagination bar')
def scroll_to_pagination_bar(page):
    logger.info("Scrolling to pagination bar")
    common = CommonPage(page)
    page.locator(common.pagination_bar).scroll_into_view_if_needed()

@when('the user clicks the "Last" button')
def click_last(page):
    logger.info("Clicking the Last button")
    common = CommonPage(page)
    common.click_last()

@when('the user clicks the last page button')
def click_last_page_button(page):
    logger.info("Clicking the last page button")
    common = CommonPage(page)
    common.click_last()

@then('the movie list should update with new content')
def movie_list_should_update(page, context={}):
    logger.info("Checking that the movie list updated with new content")
    common = CommonPage(page)
    new_first_title = common.get_first_movie_title()
    logger.info(f"New first movie title: {new_first_title}")
    assert new_first_title not in (None, ""), "New first movie title is empty or None!"
    assert new_first_title != context.get('first_title'), "Movie list did not update after pagination"

@then('the user should see the last page of results')
def should_see_last_page(page):
    logger.info("Verifying the user is on the last page of results")
    common = CommonPage(page)
    assert common.is_last_page(), "Not on the last page of results"
