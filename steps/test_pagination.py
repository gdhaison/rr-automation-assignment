import os
from pytest_bdd import scenarios, given, when, then, parsers
from pages.home_page import HomePage
from pages.common_page import CommonPage
from utils.logger import get_logger
from utils.api_helper import get_popular_movies

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
def note_first_movie_title(page, context):
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
def movie_list_should_update(page, context):
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

@given(parsers.parse('the user verifies the movie API for page {page_num:d}'))
def verify_movie_api(page_num, context):
    data = get_popular_movies(page_num)
    assert 'results' in data and isinstance(data['results'], list), "API response missing 'results' list"
    assert len(data['results']) > 0, "API returned empty results list"
    assert data["results"][0].get("title") == context.get("first_title"), "First movie title does not match"

@when('user reload page')
def reload_page(page, context):
    logger.info("Reloading the page and noting the first movie title after reload")
    common = CommonPage(page)
    page.reload()

@then("the movie list shouldn't update with new content")
def movie_list_should_not_update(page, context):
    common = CommonPage(page)
    context['first_title_after'] = common.get_first_movie_title()
    logger.info("Checking that the movie list did NOT update after reload")
    logger.info(f"First movie title before: {context.get('first_title')}")
    logger.info(f"First movie title after: {context.get('first_title_after')}")
    assert context.get('first_title_after') == context.get('first_title'), "Movie list did not remain the same after the action!"

@when('the user clicks the "Previous" button')
def click_previous(page):
    logger.info("Clicking the Previous button")
    common = CommonPage(page)
    common.click_previous()

@when('the user clicks back button of the browser')
def click_back_button(page):
    logger.info("Clicking the back button of the browser")
    page.go_back()