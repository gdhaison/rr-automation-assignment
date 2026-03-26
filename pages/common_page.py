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
        # Checks if the Next button is disabled (common pattern for last page)
        return self.page.locator(self.disabled_next).is_visible()
