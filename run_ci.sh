#!/bin/bash
set -e
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

# Create and activate venv
echo "[CI] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

# Install Python dependencies
echo "[CI] Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "[CI] Installing Playwright browsers..."
python -m playwright install --with-deps

# Install Node.js dependencies
echo "[CI] Installing Node.js dependencies..."
npm install

# Run tests and generate reports
echo "[CI] Running tests..."
if [ -n "$TAG" ]; then
  python -m pytest -v -s -m "$TAG" --alluredir="$ALLURE_RESULTS_DIR" --cucumberjson="$CUCUMBER_JSON" | tee "$LOG_FILE"
else
  python -m pytest -v -s --alluredir="$ALLURE_RESULTS_DIR" --cucumberjson="$CUCUMBER_JSON" | tee "$LOG_FILE"
fi

echo "Cucumber JSON report generated at $CUCUMBER_JSON"

# Automatically generate Cucumber HTML report if cucumber-html-reporter is available
if [ -f node_modules/cucumber-html-reporter/package.json ]; then
  node -e "const r=require('cucumber-html-reporter');r.generate({theme:'bootstrap',jsonFile:'$CUCUMBER_JSON',output:'$CUCUMBER_HTML',reportSuiteAsScenarios:true,launchReport:false});console.log('Cucumber HTML report generated at $CUCUMBER_HTML')"
else
  echo "cucumber-html-reporter not found. Run 'npm install cucumber-html-reporter' to enable HTML report generation."
fi