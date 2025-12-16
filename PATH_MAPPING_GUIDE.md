# Client-Side Path Mapping for Playwright Scripts

## The Problem

When someone else runs tests and posts failures to your triage engine:
- Their playwright script URL: `file:///C:/their-computer/tests/login.spec.js#L14`
- This won't work on YOUR machine because you don't have `C:/their-computer/tests/`

## The Solution: Client-Side Path Mapping

Instead of them knowing your local path (impossible!), **YOU** map their paths to yours when viewing results.

## How to Use

### 1. Configure Your Local Path

Edit [`view_results_local.py`](file:///c:/bug-triage-engine/view_results_local.py) and set your local test files path:

```python
YOUR_LOCAL_BASE_PATH = "C:/my-projects/tests"  # ← Change this!
```

### 2. Run the Viewer

```bash
python view_results_local.py
```

### 3. See Mapped URLs

The script will show you BOTH URLs:

```
--- PLAYWRIGHT SCRIPT URLS ---
Remote (theirs):  file:///C:/their-computer/tests/login.spec.js#L14
Local (yours):    file:///C:/my-projects/tests/login.spec.js#L14

👆 Click the LOCAL URL to open the file on YOUR system!
```

## How It Works

```
┌─────────────────────────────────────────────────────────────┐
│ 1. QA Engineer posts test failure                          │
│    File: C:/their-computer/tests/login.spec.js             │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 2. Triage Engine stores it                                 │
│    URL: file:///C:/their-computer/tests/login.spec.js#L14  │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 3. YOU retrieve results with view_results_local.py         │
│    Your config: YOUR_LOCAL_BASE_PATH = "C:/my-tests"       │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│ 4. Script maps to YOUR path                                │
│    Extracts filename: "login.spec.js"                       │
│    Maps to: C:/my-tests/login.spec.js                      │
│    Shows: file:///C:/my-tests/login.spec.js#L14            │
└─────────────────────────────────────────────────────────────┘
```

## Requirements

For this to work, you need:

1. **Same test files** - You must have the same test files (e.g., via Git)
2. **Same filenames** - The filenames must match (e.g., `login.spec.js`)
3. **Your local path** - Configure where YOUR test files are located

## Example Workflow

### QA Team Setup
```bash
# QA engineer clones repo
git clone https://github.com/company/qa-tests.git
cd qa-tests

# Runs tests (they fail)
npx playwright test

# Posts failures to your triage engine
python post_failures.py
```

### Your Setup
```bash
# You clone the SAME repo
git clone https://github.com/company/qa-tests.git C:/my-projects/tests

# Configure view_results_local.py
YOUR_LOCAL_BASE_PATH = "C:/my-projects/tests"

# View results with mapped paths
python view_results_local.py
```

Now when you click the LOCAL URL, it opens the file on YOUR machine!

## Alternative: Use Original Viewer

If you don't need path mapping (e.g., you're viewing your own test results), use the original viewer:

```bash
python view_results.py
```

This shows the URLs as-is without any mapping.
