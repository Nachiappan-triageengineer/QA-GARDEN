# Demo Playwright Script for Bug Triage Engine

## Overview

This demo includes a Playwright test suite (`demo.spec.js`) with intentional failures to demonstrate the bug triage engine's capabilities.

## Setup

### 1. Install Playwright

```bash
npm init playwright@latest
```

Or if you already have a package.json:

```bash
npm install -D @playwright/test
npx playwright install
```

### 2. Files Included

- **`demo.spec.js`** - Test suite with 15 tests (12 failing, 3 passing)
- **`playwright.config.js`** - Configuration to generate JSON reports

## Running the Demo

### Step 1: Run Playwright Tests

```bash
npx playwright test demo.spec.js
```

This will:
- Execute all tests in `demo.spec.js`
- Generate `playwright-report.json` with failure details
- Take screenshots on failures
- Record videos on failures

### Step 2: Process Failures with Triage Engine

The `playwright-report.json` file contains structured failure data that can be converted to the triage engine format.

#### Manual Processing

You can manually extract failure data from `playwright-report.json` and POST to the triage API:

```bash
curl -X POST http://localhost:8003/api/triage \
  -H "Content-Type: application/json" \
  -d '{
    "test_name": "should display correct page title",
    "file_path": "demo.spec.js",
    "error_message": "expect(page).toHaveTitle expected",
    "stack_trace": "at demo.spec.js:14:5",
    "logs": "",
    "llm_model": "gemma:2b",
    "bert_url": "http://localhost:8001/triage",
    "labels": ["frontend", "ui"]
  }'
```

### Step 3: View Results

```bash
python view_results.py
```

## Test Categories

The demo includes failures across different categories:

### 🔐 Login Page Tests (3 tests)
- Page title mismatch
- Missing login button
- Missing email input

### 📊 Dashboard Tests (2 tests)
- Missing user profile element
- Incorrect welcome message

### 📝 Form Submission Tests (2 tests)
- Missing form elements
- Missing error validation

### 🧭 Navigation Tests (2 tests)
- Missing navigation links
- Missing breadcrumbs

### 🌐 API Integration Tests (2 tests)
- API endpoint failures
- 404 handling

### ✅ Passing Tests (3 tests)
- Successful page loads
- Working todo functionality

## Expected Output

After running the tests, you should see:

```
Running 15 tests using 1 worker

  ✓  should load the demo page successfully
  ✓  should have input field for new todos
  ✓  should add a new todo item
  ✗  should display correct page title
  ✗  should find login button
  ✗  should validate email input
  ✗  should load user profile
  ✗  should display welcome message
  ✗  should submit contact form
  ✗  should validate required fields
  ✗  should navigate to settings page
  ✗  should have working breadcrumbs
  ✗  should fetch user data
  ✗  should handle 404 errors gracefully

  12 failed
  3 passed
```

## Triage Engine Integration

The failures will be categorized by the triage engine as:

- **Frontend UI** - Element not found, selector issues
- **Backend API** - API endpoint failures
- **Performance** - Timeout issues
- **Unknown** - Other failures

Each failure will receive:
- ✅ **Title** - Generated bug title
- ✅ **Description** - Detailed bug description
- ✅ **Error Line** - Line number from stack trace
- ✅ **Playwright Script** - File path (demo.spec.js)
- ✅ **Status** - "failed"
- ✅ **Stack Trace** - Full error stack trace

## Next Steps

1. **Run the tests**: `npx playwright test demo.spec.js`
2. **Start triage API**: `python main.py`
3. **Process failures**: Extract from `playwright-report.json` and POST to API
4. **View results**: `python view_results.py`

## Customization

You can modify `demo.spec.js` to:
- Add more test scenarios
- Change the target website
- Adjust failure types
- Add more passing tests

Enjoy testing the bug triage engine! 🚀
