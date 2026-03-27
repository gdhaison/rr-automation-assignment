from utils.logger import get_logger

class CommonPage:
    def __init__(self, page):
        self.page = page
        self.next_button = 'a[aria-label="Next page"]'
        self.prev_button = 'a[aria-label="Previous page"]'
        self.last_page_btn = '//li[@class="next"]/preceding-sibling::li[1]'
        self.movie_title = """//div[@id='root']//div[img]/p[contains(@class, 'font-bold')]"""
        self.pagination_bar = '#react-paginate'
        self.active_page = '.selected > a'
        self.disabled_next = 'button[aria-label="Next"][disabled]'
        self.dynamic_container = '//div[contains(text(), "{text}")]'
        self.movie_genre = "//div[@class='flex flex-col items-center']/p[2]"

        self.year_from_input = '(//span[@aria-live="polite"])[3]'
        self.year_to_input = '(//span[@aria-live="polite"])[4]'

        self.dynamic_star = "(//div[@aria-posinset={star}]/div)[{half}]"
        self.dynamic_star_parent = "(//div[@aria-posinset={star}]/div)[{half}]/parent::div"
        self.dynamic_text = '//*[contains(text(), "{text}")]'

    def click_next(self):
        self.page.click(self.next_button)

    def click_previous(self):
        self.page.click(self.prev_button)

    def click_last(self):
        self.page.click(self.last_page_btn)

    def get_first_movie_title(self):
        first = self.page.locator(self.movie_title).first
        try:
            first.wait_for(state="visible", timeout=10000)
        except Exception:
            raise AssertionError("Expected at least one movie title to be visible, but none were found.")
        return (first.text_content() or "").strip()
        

    def is_last_page(self):
        return self.page.locator(self.disabled_next).is_visible()


    def select_genre_by_text(self, genre_text: str):
        self.page.click(self.dynamic_container.format(text="Select"))
        option = self.dynamic_container.format(text=genre_text)
        self.page.click(option)

    def get_selected_genre(self) -> str:
        genres_locator = self.page.locator(self.movie_genre)
        genres = genres_locator.all_text_contents()
    
        return [g.strip() for g in genres]
    
    def set_year_range(self, year_from: str, year_to: str):
        self.page.click(self.dynamic_container.format(text="1900"))
        self.page.click(self.dynamic_container.format(text=str(year_from)))
        self.page.click(self.dynamic_container.format(text="2025"))
        self.page.click(self.dynamic_container.format(text=str(year_to)))

        # Wait for the UI to update
        self.page.wait_for_timeout(3000)
    
    def select_rating_by_text(self, rating_text: str):
        star = float(rating_text)
        half = 2
        if star % 1 == 0.5:
            star += 0.5
            half = 1

        rating_locator = self.dynamic_star.format(star=int(star), half=half)
        self.page.click(rating_locator)

    def get_selected_rating_aria(self, rating_text: str) -> str:
        star = float(rating_text)
        half = 2
        if star % 1 == 0.5:
            star += 0.5
            half = 1

        rating_locator = self.dynamic_star_parent.format(star=int(star), half=half)
        logger = get_logger("test_filter")
        logger.info(f"Checking aria-checked for rating '{rating_text}': {rating_locator}")

        return self.page.locator(rating_locator).get_attribute("aria-checked")

    def click_to_text(self, text: str):
        logger = get_logger("test_filter")
        logger.info(f"Clicking on text: {text}")
        self.page.click(self.dynamic_text.format(text=text))
