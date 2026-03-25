#!/bin/zsh
REPORT_NAME="report-$(date +%Y%m%d-%H%M%S)"
REPORT_DIR="reports/$REPORT_NAME"
ALLURE_RESULTS_DIR="$REPORT_DIR/allure-results"
CUCUMBER_JSON="$REPORT_DIR/cucumber-report.json"
CUCUMBER_HTML="$REPORT_DIR/cucumber-report.html"
mkdir -p "$REPORT_DIR"
export REPORT_NAME
export ALLURE_RESULTS_DIR
LOG_FILE="$REPORT_DIR/test.log"
TAG=${TAG:-}
if [ -n "$TAG" ]; then
  .venv/bin/pytest -v -s -m "$TAG" --alluredir="$ALLURE_RESULTS_DIR" --cucumberjson="$CUCUMBER_JSON" | tee "$LOG_FILE"
else
  .venv/bin/pytest -v -s --alluredir="$ALLURE_RESULTS_DIR" --cucumberjson="$CUCUMBER_JSON" | tee "$LOG_FILE"
fi

echo "Cucumber JSON report generated at $CUCUMBER_JSON"

# Automatically generate Cucumber HTML report if cucumber-html-reporter is available
if [ -f node_modules/cucumber-html-reporter/package.json ]; then
  node -e "const r=require('cucumber-html-reporter');r.generate({theme:'bootstrap',jsonFile:'$CUCUMBER_JSON',output:'$CUCUMBER_HTML',reportSuiteAsScenarios:true,launchReport:false});console.log('Cucumber HTML report generated at $CUCUMBER_HTML')"
else
  echo "cucumber-html-reporter not found. Run 'npm install cucumber-html-reporter' to enable HTML report generation."
fi
