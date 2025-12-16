# Simple Instructions for QA Person

## Where to Send the Playwright Script URL

**API URL:** `http://192.168.1.13:8003/api/triage`

Use **Option 1: Post a Triage Input**

---

## What to Send

Just send the playwright script URL in the `playwright_script_url` field:

```json
{
    "test_name": "Login test failed",
    "file_path": "tests/login.spec.js",
    "error_message": "Timeout waiting for element",
    "stack_trace": "at login.spec.js:25:5",
    "logs": "Test started...",
    "llm_model": "gemma:2b",
    "bert_url": "http://localhost:8001/triage",
    "labels": ["ui", "login"],
    "test_url": "https://example.com/login",
    "playwright_script_url": "file:///C:/qa-tests/login.spec.js#L25"
}
```

The important field is:
```json
"playwright_script_url": "file:///C:/qa-tests/login.spec.js#L25"
```

That's it! Just paste the playwright script URL there.
