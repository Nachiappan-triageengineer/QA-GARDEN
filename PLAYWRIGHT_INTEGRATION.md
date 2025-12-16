# Playwright + Triage Engine Integration Guide

## 🎯 Overview

This integration automatically runs Playwright tests and sends failures to your bug triage engine.

---

## 📦 Setup

### 1. Install Playwright

```bash
# Install Node.js dependencies
npm install

# Install Playwright browsers
npx playwright install
```

### 2. Verify Files

Make sure you have:
- ✅ `demo.spec.js` - Playwright test file
- ✅ `playwright.config.js` - Playwright configuration
- ✅ `run_playwright_and_triage.py` - Integration script
- ✅ `package.json` - Node.js dependencies

---

## 🚀 Usage

### Option 1: Automated (Recommended)

**Single command to run tests and triage:**

```bash
python run_playwright_and_triage.py
```

This will:
1. ✅ Run Playwright tests (`demo.spec.js`)
2. ✅ Generate `playwright-report.json`
3. ✅ Parse the report for failures
4. ✅ Post each failure to the triage engine
5. ✅ Display results

**Output:**
```
================================================================================
PLAYWRIGHT + TRIAGE ENGINE INTEGRATION
================================================================================

================================================================================
Running Playwright Tests
================================================================================

Test execution completed!
Exit code: 1
✓ Report generated: playwright-report.json

================================================================================
Parsing Test Results
================================================================================

Found 12 failed test(s)

================================================================================
Posting Failures to Triage Engine
================================================================================

[1/12] should display correct page title
--------------------------------------------------------------------------------
✓ SUCCESS
  Title: Page Title Mismatch in TodoMVC Application
  Error Line: 14
  Playwright Script: demo.spec.js
  ID: 1702469980_abc123

...

================================================================================
SUMMARY
================================================================================
✓ Successfully triaged: 12
✗ Failed to triage: 0
Total failures: 12
```

---

### Option 2: Step by Step

**Step 1: Run Playwright tests manually**
```bash
npx playwright test demo.spec.js
```

**Step 2: Check the report**
```bash
# View the JSON report
type playwright-report.json
```

**Step 3: Run the integration script**
```bash
python run_playwright_and_triage.py
```

---

### Option 3: Using npm Scripts

```bash
# Run tests only
npm test

# Run demo tests
npm run test:demo

# Run tests with JSON reporter
npm run test:report
```

---

## 📊 How It Works

### Data Flow

```
┌──────────────────┐
│  demo.spec.js    │  ← Your Playwright tests
└────────┬─────────┘
         │
         │ npx playwright test
         ▼
┌──────────────────────────┐
│  Playwright Execution    │
│  - Runs tests            │
│  - Captures failures     │
│  - Takes screenshots     │
└────────┬─────────────────┘
         │
         │ Generates
         ▼
┌──────────────────────────┐
│  playwright-report.json  │  ← JSON report with all test results
└────────┬─────────────────┘
         │
         │ Parsed by
         ▼
┌──────────────────────────────┐
│  run_playwright_and_triage.py│
│  - Extracts failures         │
│  - Formats for triage API    │
└────────┬─────────────────────┘
         │
         │ HTTP POST
         ▼
┌──────────────────────────────┐
│  Triage Engine API           │
│  http://localhost:8003       │
│  - Generates bug titles      │
│  - Extracts error lines      │
│  - Stores results            │
└────────┬─────────────────────┘
         │
         │ Returns
         ▼
┌──────────────────────────────┐
│  Triaged Results             │
│  {                           │
│    "title": "...",           │
│    "error_line": 14,         │
│    "playwright_script": "..." │
│  }                           │
└──────────────────────────────┘
```

---

## 🔧 Customization

### Add Your Own Tests

1. Create a new test file:
```javascript
// my-tests.spec.js
const { test, expect } = require('@playwright/test');

test('my custom test', async ({ page }) => {
  await page.goto('https://example.com');
  await expect(page).toHaveTitle('My Expected Title');
});
```

2. Update `run_playwright_and_triage.py`:
```python
TEST_FILE = "my-tests.spec.js"  # Change this line
```

3. Run:
```bash
python run_playwright_and_triage.py
```

---

### Change API URL

Edit `run_playwright_and_triage.py`:
```python
API_URL = "http://your-server:8003/api/triage"
```

---

### Modify Test Labels

Edit `run_playwright_and_triage.py`:
```python
"labels": ["playwright", "automated", "ui", "regression"]  # Add your labels
```

---

## 📁 File Structure

```
bug-triage-engine/
├── demo.spec.js                    ← Playwright tests
├── playwright.config.js            ← Playwright config
├── run_playwright_and_triage.py   ← Integration script
├── package.json                    ← Node.js dependencies
├── playwright-report.json          ← Generated test report
├── main.py                         ← Triage API server
├── view_results.py                 ← View triage results
└── app/
    ├── api/routes.py              ← API endpoints
    ├── services/triage_service.py ← Triage logic
    └── schemas.py                 ← Data models
```

---

## 🎯 Complete Workflow Example

```bash
# Terminal 1: Start the triage engine
python main.py

# Terminal 2: Run tests and auto-triage
python run_playwright_and_triage.py

# View results
python view_results.py

# Or in browser
start http://192.168.1.51:8003/api/triage
```

---

## 🐛 Troubleshooting

### Playwright not installed?
```bash
npm install -D @playwright/test
npx playwright install
```

### API not running?
```bash
# Start the triage engine first
python main.py
```

### No failures found?
```bash
# Check if tests actually failed
npx playwright test demo.spec.js

# Check the report
type playwright-report.json
```

### Import errors?
```bash
# Install Python dependencies
pip install requests
```

---

## ✅ Success Checklist

- [ ] Playwright installed (`npx playwright --version`)
- [ ] Triage API running (`python main.py`)
- [ ] Tests run successfully (`npx playwright test demo.spec.js`)
- [ ] Report generated (`playwright-report.json` exists)
- [ ] Integration script works (`python run_playwright_and_triage.py`)
- [ ] Results visible (`python view_results.py`)

---

## 🚀 Next Steps

1. **Add more tests** to `demo.spec.js`
2. **Create test suites** for different features
3. **Set up CI/CD** to run this automatically
4. **Customize labels** for better categorization
5. **Export results** to JIRA, GitHub Issues, etc.

Happy testing! 🎉
