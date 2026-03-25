class CommonPage:
    def __init__(self, page):
        self.page = page
        self.next_button = 'button[aria-label="Next"]'
        self.prev_button = 'button[aria-label="Previous"]'
        self.last_page_btn = '//li[@class="next"]/preceding-sibling::li[1]'
        self.movie_title = """//div[@id='root']//div[img]/p[contains(@class, 'font-bold')]"""
        self.pagination_bar = '#react-paginate'
        self.active_page = '.selected > a'
        self.disabled_next = 'button[aria-label="Next"][disabled]'

    def click_next(self):
        self.page.click(self.next_button)

    def click_prev(self):
        self.page.click(self.prev_button)

    def click_last(self):
        self.page.click(self.last_page_btn)

    def get_first_movie_title(self):
        # Check if the last page button is visible before trying to get the movie title
        if not self.page.locator(self.movie_title).is_visible():
            raise AssertionError('Expected last page contains data, but it is not.')
        return self.page.locator(self.movie_title).first.text_content()

    def is_last_page(self):
        # Checks if the Next button is disabled (common pattern for last page)
        return self.page.locator(self.disabled_next).is_visible()
