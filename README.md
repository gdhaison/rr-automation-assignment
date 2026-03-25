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

## Node.js Setup (for Cucumber HTML report)

1. Install Node.js if you haven't already: https://nodejs.org/
2. Install the required npm package (run once in project root):
   ```sh
   npm install cucumber-html-reporter
   ```

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

2. Convert Allure results to Cucumber JSON:
   ```sh
   npx allure-cucumber-json --allureResults=reports/<timestamp>/allure-results --output=reports/<timestamp>/cucumber-report.json
   ```
   Replace `<timestamp>` with your actual report folder name.

3. Create a Node.js script (e.g., `create-report.js`) with:
   ```js
   const reporter = require('cucumber-html-reporter');
   reporter.generate({
     theme: 'bootstrap',
     jsonFile: 'reports/<timestamp>/cucumber-report.json',
     output: 'reports/<timestamp>/cucumber-report.html',
     reportSuiteAsScenarios: true,
     launchReport: true,
   });
   ```

4. Run the script:
   ```sh
   node create-report.js
   ```

This will generate and open a Cucumber HTML report from your Allure results.
