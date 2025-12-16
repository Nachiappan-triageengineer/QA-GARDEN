# Setup Instructions for QA Team / Other Users

## Where to Send Test Failures

**API URL:** `http://192.168.1.13:8003/api/triage`

Send your test failures to this URL using a POST request.

---

## Example: How to Send a Test Failure

```python
import requests

# Your triage engine API
API_URL = "http://192.168.1.13:8003/api/triage"

# Test failure data
failure = {
    "test_name": "should display login page",
    "file_path": "tests/login.spec.js",  # Your test file path
    "error_message": "expect(page).toHaveTitle(expected)\n\nExpected: 'Login'\nReceived: 'Home'",
    "stack_trace": "at tests/login.spec.js:25:5\n    at WorkerRunner...",
    "logs": "[2025-12-16] DEBUG: Navigating to https://example.com/login\n[2025-12-16] ERROR: Title assertion failed",
    "llm_model": "gemma:2b",
    "bert_url": "http://localhost:8001/triage",
    "labels": ["ui", "playwright"],
    "test_url": "https://example.com/login"  # The URL you were testing
}

# Send to triage engine
response = requests.post(API_URL, json=failure)
print(response.json())
```

---

## Required Fields

| Field | Description | Example |
|-------|-------------|---------|
| `test_name` | Name of the test | `"should login successfully"` |
| `file_path` | Test file path | `"tests/login.spec.js"` |
| `error_message` | Error message | `"Timeout waiting for selector"` |
| `stack_trace` | Stack trace | `"at login.spec.js:25:5..."` |
| `logs` | Test logs | `"[INFO] Starting test..."` |
| `llm_model` | LLM model to use | `"gemma:2b"` |
| `bert_url` | BERT service URL | `"http://localhost:8001/triage"` |
| `labels` | Tags for categorization | `["ui", "playwright"]` |
| `test_url` | URL being tested | `"https://example.com/login"` |

---

## That's It!

Just POST your test failures to `http://192.168.1.13:8003/api/triage` and the triage engine will:
- Generate bug title and description
- Extract error line number
- Create clickable playwright script URL
- Store the result for viewing
