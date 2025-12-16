"""
Demo: Sample Playwright failures in triage engine format
This shows how to format Playwright test failures for the bug triage API
"""
import requests
import json

API_URL = "http://192.168.1.13:8003/api/triage"

# Sample failures from demo.spec.js in the correct format
sample_failures = [
    {
        "test_name": "should display correct page title",
        "file_path": "demo.spec.js",
        "error_message": "expect(page).toHaveTitle(expected)\n\nExpected string: \"Login - MyApp\"\nReceived string: \"TodoMVC\"",
        "stack_trace": """    at demo.spec.js:14:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:30:15] INFO: Starting test: should display correct page title\n[2025-12-13 15:30:16] DEBUG: Navigating to https://demo.playwright.dev/todomvc\n[2025-12-13 15:30:17] ERROR: Title assertion failed\n[2025-12-13 15:30:18] INFO: Screenshot saved to test-results/",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["frontend", "ui", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    },
    {
        "test_name": "should find login button",
        "file_path": "demo.spec.js",
        "error_message": "page.click: Timeout 30000ms exceeded.\nwaiting for locator(\"#login-button\")\nNote: locator resolved to <empty>",
        "stack_trace": """    at demo.spec.js:20:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:30:20] INFO: Starting test: should find login button\n[2025-12-13 15:30:21] DEBUG: Navigating to https://demo.playwright.dev/todomvc\n[2025-12-13 15:30:22] DEBUG: Attempting to click #login-button\n[2025-12-13 15:30:52] ERROR: Timeout waiting for selector #login-button",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["frontend", "ui", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    },
    {
        "test_name": "should validate email input",
        "file_path": "demo.spec.js",
        "error_message": "expect(locator).toBeVisible()\n\nLocator: locator('#email-input')\nExpected: visible\nReceived: <element(s) not found>",
        "stack_trace": """    at demo.spec.js:27:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:30:55] INFO: Starting test: should validate email input\n[2025-12-13 15:30:56] DEBUG: Navigating to https://demo.playwright.dev/todomvc\n[2025-12-13 15:30:57] DEBUG: Looking for #email-input\n[2025-12-13 15:30:58] ERROR: Element #email-input not found",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["frontend", "ui", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    },
    {
        "test_name": "should load user profile",
        "file_path": "demo.spec.js",
        "error_message": "page.waitForSelector: Timeout 5000ms exceeded.\nwaiting for locator(\".user-profile\")",
        "stack_trace": """    at demo.spec.js:37:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:31:00] INFO: Starting test: should load user profile\n[2025-12-13 15:31:01] DEBUG: Navigating to https://demo.playwright.dev/todomvc\n[2025-12-13 15:31:02] DEBUG: Waiting for .user-profile\n[2025-12-13 15:31:07] ERROR: Timeout after 5000ms",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["frontend", "ui", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    },
    {
        "test_name": "should display welcome message",
        "file_path": "demo.spec.js",
        "error_message": "expect(locator).toContainText(expected)\n\nLocator: locator('h1')\nExpected string: \"Welcome, User!\"\nReceived: \"todos\"",
        "stack_trace": """    at demo.spec.js:43:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:31:10] INFO: Starting test: should display welcome message\n[2025-12-13 15:31:11] DEBUG: Navigating to https://demo.playwright.dev/todomvc\n[2025-12-13 15:31:12] DEBUG: Checking h1 text content\n[2025-12-13 15:31:13] ERROR: Text mismatch - expected 'Welcome, User!' but got 'todos'",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["frontend", "ui", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    },
    {
        "test_name": "should submit contact form",
        "file_path": "demo.spec.js",
        "error_message": "page.click: Timeout 30000ms exceeded.\nwaiting for locator(\"#submit-contact\")\nNote: locator resolved to <empty>",
        "stack_trace": """    at demo.spec.js:53:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:31:15] INFO: Starting test: should submit contact form\n[2025-12-13 15:31:16] DEBUG: Navigating to https://demo.playwright.dev/todomvc\n[2025-12-13 15:31:17] DEBUG: Filling form fields\n[2025-12-13 15:31:18] ERROR: Submit button #submit-contact not found",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["frontend", "ui", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    },
    {
        "test_name": "should fetch user data",
        "file_path": "demo.spec.js",
        "error_message": "expect(received).toBe(expected)\n\nExpected: 200\nReceived: 404",
        "stack_trace": """    at demo.spec.js:76:5
    at WorkerRunner._runTestWithBeforeHooks (/node_modules/@playwright/test/lib/worker/workerRunner.js:471:7)
    at async WorkerRunner.runTest (/node_modules/@playwright/test/lib/worker/workerRunner.js:395:7)""",
        "logs": "[2025-12-13 15:31:20] INFO: Starting test: should fetch user data\n[2025-12-13 15:31:21] DEBUG: Making GET request to /api/user/123\n[2025-12-13 15:31:22] ERROR: API returned 404 Not Found\n[2025-12-13 15:31:23] DEBUG: Response body: {\"error\":\"Not found\"}",
        "llm_model": "gemma:2b",
        "bert_url": "http://localhost:8001/triage",
        "labels": ["backend", "api", "playwright"],
        "test_url": "https://demo.playwright.dev/todomvc"
    }
]

def post_sample_failures():
    """Post all sample failures to the triage API"""
    print("=" * 80)
    print("Posting Demo Playwright Failures to Triage Engine")
    print("=" * 80)
    print()
    
    success_count = 0
    failed_count = 0
    
    for i, failure in enumerate(sample_failures, 1):
        print(f"\n[{i}/{len(sample_failures)}] Processing: {failure['test_name']}")
        print("-" * 80)
        
        try:
            response = requests.post(API_URL, json=failure, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            print(f"✓ SUCCESS!")
            print(f"  Title: {result.get('title', 'N/A')}")
            print(f"  Error Line: {result.get('error_line', 'N/A')}")
            print(f"  Status: {result.get('status', 'N/A')}")
            print(f"  Result ID: {result.get('id', 'N/A')}")
            success_count += 1
            
        except requests.exceptions.ConnectionError:
            print(f"✗ ERROR: Cannot connect to API at {API_URL}")
            print("  Make sure the triage engine is running: python main.py")
            failed_count += 1
            
        except requests.exceptions.Timeout:
            print(f"✗ ERROR: Request timed out (LLM might be slow)")
            failed_count += 1
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            failed_count += 1
    
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Successful: {success_count}")
    print(f"✗ Failed: {failed_count}")
    print(f"Total: {len(sample_failures)}")
    print()
    print("View results with: python view_results.py")
    print("=" * 80)

def print_sample_format():
    """Print one sample in JSON format for reference"""
    print("\n" + "=" * 80)
    print("SAMPLE FORMAT (First Failure)")
    print("=" * 80)
    print(json.dumps(sample_failures[0], indent=2))
    print()

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--format":
        print_sample_format()
    else:
        post_sample_failures()
