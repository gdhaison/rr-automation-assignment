# rr-automation-assignment

## Setup

1. Create and activate a virtual environment:
   ```sh
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```

3. Install Playwright browsers:
   ```sh
   python -m playwright install
   ```

4. Clone .env.example to .env and update the values as needed.
   ```
   cp .env.example .env
   ```

## Node.js Setup (for Cucumber HTML report)

1. Install Node.js if you haven't already: https://nodejs.org/
2. Install the required npm package (run once in project root):
   ```sh
   npm install cucumber-html-reporter
   ```

## Allure Reporting

- Allure results are saved in each run's `reports/<timestamp>/allure-results` folder.
- To view the Allure report locally, install Allure commandline and run:
  ```sh
  allure serve reports/<timestamp>/allure-results
  ```
- In CI, the Allure HTML report is generated and uploaded as an artifact.
- Failed tests will have screenshots and logs attached in the Allure report.

### Install Allure commandline (macOS):
```sh
brew install allure
```

See https://docs.qameta.io/allure/ for more info.

To generate a Cucumber HTML report from your Allure results:

1. Install Node.js and cucumber-html-reporter globally (if not already):
   ```sh
   npm install -g cucumber-html-reporter allure-cucumber-json
   ```

This will generate and open a Cucumber HTML report from your Allure results.

## Running Tests

To run all tests:
```sh
./run.sh
```

To run tests by tag (e.g., only @pagination):
```sh
TAG=pagination ./run.sh
```

After each test run, both Cucumber JSON and HTML reports are generated automatically in the corresponding `reports/<timestamp>/` folder.

- To view the Cucumber HTML report, open:
  ```
  reports/<timestamp>/cucumber-report.html
  ```

Test reports and logs are saved in the `reports/` folder, organized by timestamp.

## CI/CD Integration
CI implementation can be achieved by incorporating the following steps:
1. Create new Pull Requests (PRs)
2. Tests are automatically triggered on each PR
3. Reports are generated and uploaded as artifacts (Can be viewed in the CI/CD pipeline)

# Test case checklist
Feature File Checklist
1. filter.feature — Discover Filters (Type, Genre, Year, Ratings)
Covers:
* Filtering movies/TV shows by type (Movie, TV Show)
* Filtering by genre (e.g., Animation)
* Filtering by year range (from, to, or same year)
* Filtering by minimum rating (e.g., 4 stars & up)
* Verifying that UI results match TMDB API responses for the applied filters
* Ensuring filters persist across pagination
Future Cases to Implement:
* Filtering by multiple genres simultaneously
* Combining all filters (type, genre, year, rating) in a single scenario
* Edge cases: invalid year ranges, no results, or filters with no matching content
* Verifying filter reset/clear functionality
* Accessibility checks for filter controls

2. pagination.feature — Pagination
Covers:
* Navigating to next/previous/last pages in the result list
* Verifying that the result list updates correctly when paginating
* Ensuring the active page indicator updates
* Checking that filters persist when navigating between pages
Future Cases to Implement:
* Jumping to a specific page number
* Handling pagination when the result set is small (single page)
* Verifying correct behavior when paginating with active filters
* Testing pagination controls' accessibility (keyboard navigation, ARIA labels)


## Defect found
* Pagination:
   - Reload Page error:
      Expected:
         Given the user is on the second page of results
         When the user reloads the page
         Then the user should remain on the second page of results
      Actual:
         The user is redirected to error page

   - Click back button:
      Expected:
         Given the user is on the second page of results
         When the user clicks the back button
         Then the user should return to the first page of results
      Actual:
         The user is redirected to the error page

   - Go to last page:
      Expected:
         Given the user is on the first page of results
         When the user clicks the last page button
         Then the user should be taken to the last page of results
      Actual:
         The user is redirected to the error page
         The pagination controls is displayed incorrectly for last page in popular screen

* Filter
   - Apply Genre Filter:
      Expected:
         Given the user is on the popular movies page
         When the user selects the "Animation" genre filter
         Then the movie list should update to show "animation" text in description of the movie
      Actual:
         The movie list is not updated correctly to show "animation" text in description of the movie

   - Apply Year Range Filter:
      Expected:
         Given the user is on the popular movies page
         When the user sets the year range filter from "2010" to "2020"
         Then the movie list should update to show only movies released between 2010 and 2020
      Actual:
         The movie list is not updated correctly to show only movies released between 2010 and 2020

   - Apply filter with same year:
      Expected:
         Given the user is on the popular movies page
         When the user sets the year range filter from "2020" to "2020"
         Then the movie list should update to show only movies released in 2020
      Actual:
         The movie list is not updated correctly to show only movies released in 2020

   - Filter Newest:
      Expected:
         Given the user is on the popular movies page
         When the user selects the "Newest" filter
         Then the movie list should update to show only the newest movies
      Actual:
         The movie list is not updated correctly to show only the newest movies
         (Some movie release in 2025 are displayed before 2026)

   - User call api Top rated movies:
      Expected:
         Api return response with top rated movies order by vote_average descending
      Actual:
         The movie list is not updated correctly to show movies list order by vote_average descending

* For more details of these defects, please refer to the report attached in the email