from pytest_bdd import scenarios, given, when, then, parsers
from pages.common_page import CommonPage
from utils.logger import get_logger
from utils.api_helper import get_discover_movies, get_top_rated_movies
from pages.home_page import HomePage
from utils.bdd_helpers import parse_cucumber_table

logger = get_logger("test_filter")

scenarios('../features/filter.feature')

@given('the user opens the TMDB Discover website')
def open_tmdb_home(page):
    logger.info("Opening TMDB Discover website")
    home = HomePage(page)
    home.goto()

@given(parsers.parse('the user is on the "{category}" category page'))
def on_category(page, category):
    logger.info(f"Navigating to category: {category}")
    # Implement navigation to the category if needed

@given('the user notes the title of the first item on the current list')
def note_first_item_title(page, context):
    logger.info("Noting the first item title on the current list")
    common = CommonPage(page)
    first_title = common.get_first_movie_title()
    context['first_title'] = first_title
    logger.info(f"First item title: {first_title}")

@when(parsers.parse('the user selects Genre "{genre_text}" in the Genre filter'))
def select_genre_filter(page, genre_text):
    logger.info(f"Selecting genre '{genre_text}' in Genre filter")
    common = CommonPage(page)
    common.select_genre_by_text(genre_text)

@then('the result list should update with new content')
def result_list_should_update(page, context):
    logger.info("Checking that the result list updated with new content")
    common = CommonPage(page)
    new_first_title = common.get_first_movie_title()
    assert new_first_title != context.get('first_title'), "Result list did not update after filter change"
    context['first_title'] = new_first_title

@then(parsers.parse('the Genre filter should show "{genre_text}"'))
def genre_filter_should_show(page, genre_text):
    logger.info(f"Checking that the Genre filter shows '{genre_text}'")
    common = CommonPage(page)
    genre = common.get_selected_genre()
    for g in genre:
        assert genre_text in g, f"Genre filter does not show '{genre_text}'"

@when(parsers.parse('the user verifies the discover API matches UI with filters:\n{table}'))
def verify_discover_api_matches_ui_with_filters(table, context):
    filters = parse_cucumber_table(table)

    logger.info(f"Verifying discover API with filters: {filters}")
    data = get_discover_movies(filters)
    assert 'results' in data and isinstance(data['results'], list), "API response missing 'results' list"

    for item in data['results']:
        ids = item.get('genre_ids', [])
        if filters.get('genre_id'):
            assert int(filters['genre_id']) in ids, "Genre ID does not match"
        if filters.get('vote_average_gte'):
            assert float(filters['vote_average_gte']) <= item.get('vote_average', 0), "Min rating does not match"

@then(parsers.parse('the user verifies the discover API matches UI with filters:\n{table}'))
def verify_discover_api_matches_ui_with_filters(table, context):
    filters = parse_cucumber_table(table)

    logger.info(f"Verifying discover API with filters: {filters}")
    data = get_discover_movies(filters)
    assert 'results' in data and isinstance(data['results'], list), "API response missing 'results' list"
    assert len(data['results']) > 0, "API returned empty results list"

    if filters.get('genre_id'):
        try:
            gid = int(filters['genre_id'])
        except Exception:
            gid = None
        if gid is not None:
            for item in data['results']:
                ids = item.get('genre_ids', []) or []
                assert gid in ids, f"Genre ID {gid} not present in item id={item.get('id')}"

    ui_title = context.get('first_title')
    if ui_title:
        api_titles = [(r.get('title') or r.get('name') or '').strip() for r in data['results']]
        logger.info(f"API titles sample: {api_titles[:5]}")
        assert ui_title in api_titles, f"UI first title '{ui_title}' not found in API results titles: {api_titles[:5]}"


@when(parsers.parse('the user sets Year from "{year_from}" to "{year_to}"'))
def set_year_range_step(page, year_from, year_to):
    logger.info(f"Setting year range from {year_from} to {year_to}")
    common = CommonPage(page)
    common.set_year_range(year_from, year_to)

@then(parsers.parse('the Year filter should display from "{year_from}" to "{year_to}"'))
def year_filter_should_display(page, year_from, year_to):
    logger.info(f"Checking Year filter displays {year_from} to {year_to}")
    common = CommonPage(page)
    get_selected_genre= common.get_selected_genre()
    year_from = int(year_from)
    year_to = int(year_to)
    for g in get_selected_genre:
        year = int(g.split(", ")[-1])
        assert year_from <= year <= year_to, \
            f"Year {year} is not within range {year_from}-{year_to} (Full text: {g})"

@then("the result list shouldn't update with new content")
def movie_list_should_not_update(page, context):
    common = CommonPage(page)
    context['first_title_after'] = common.get_first_movie_title()
    logger.info("Checking that the movie list did NOT update after reload")
    logger.info(f"First movie title before: {context.get('first_title')}")
    logger.info(f"First movie title after: {context.get('first_title_after')}")
    assert context.get('first_title_after') == context.get('first_title'), "Movie list did not remain the same after the action!"

@then(parsers.parse('there should be "{count}" input with value "{value}"'))
def check_input_values(page, count, value):
    count = int(count)
    value = str(value)
    logger.info(f"Checking for {count} inputs with value: {value}")
    common = CommonPage(page)
    inputs = common.page.locator(common.dynamic_container.format(text=value))
    assert inputs.count() == int(count), f"There are not {count} input fields"
    for i in range(int(count)):
        assert inputs.nth(i).input_value() == value, f"Input {i} does not have the expected value"

@when(parsers.parse('the user selects rating "{rating_text}" stars'))
def select_rating_filter(page, rating_text):
    logger.info(f"Selecting rating '{rating_text}' in Ratings filter")
    common = CommonPage(page)
    common.select_rating_by_text(rating_text)

@then(parsers.parse('the Ratings filter should show "{rating_text}" stars'))
def ratings_filter_should_show(page, rating_text):
    logger.info(f"Checking that the Ratings filter shows '{rating_text}'")
    common = CommonPage(page)
    rating = common.get_selected_rating_aria(rating_text)
    assert rating == "true"

@when(parsers.parse('the user selects "{option}" in navigation bar'))
def select_sort_option(page, option):
    logger.info(f"Selecting '{option}' in navigation bar")
    common = CommonPage(page)
    common.click_to_text(option)

@then("the Genre filter should show movies as descending order")
def genre_filter_should_show_descending_order(page):
    logger.info("Checking that the Genre filter shows movies as descending order")
    page.wait_for_timeout(5000)
    common = CommonPage(page)

    genre = common.get_selected_genre()
    result = []
    max = 0
    logger.info(f"genre: {genre}")
    for g in genre:
        year = int(g.split(", ")[-1])
        if max == 0:
            max = year

        logger.info(f"Checking year for year: {year}")
        logger.info(f"Current max year: {max}")

        assert year <= max, f"Genre filter shows movies not in descending order (Full text: {g})"
        max = year

@given("the user calls API for top rated movies")
def call_top_rated_api(page, context):
    logger.info("Calling API for top rated movies")
    common = CommonPage(page)
    res = get_top_rated_movies()
    context['api_response'] = res

@then("the API response should contain top rated movies ordered by vote_average descending")
def check_top_rated_movies_order(context):
    api_response = context.get('api_response', {})
    results = api_response.get('results', [])
    for i in range(len(results) - 1):
        assert results[i].get('vote_average', 0) >= results[i + 1].get('vote_average', 0), \
            f"Top rated movies are not sorted by vote_average descending (Found: {results[i].get('title')})"