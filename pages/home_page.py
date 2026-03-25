class HomePage:
    def __init__(self, page):
        self.page = page
        self.url = "https://tmdb-discover.surge.sh/"

    def goto(self):
        self.page.goto(self.url)
