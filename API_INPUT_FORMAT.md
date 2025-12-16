# Triage API Input Format

## POST Endpoint
`http://192.168.1.13:8003/api/triage`

## Required Fields

```json
{
  "test_name": "",
  "file_path": "",
  "error_message": "",
  "stack_trace": "",
  "logs": "",
  "llm_model": "gemma:2b",
  "bert_url": "http://127.0.0.1:8001",
  "labels": [],
  "test_url": "",
  "playwright_script_url": ""
}
```

## Field Descriptions

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `test_name` | string | Yes | Test name |
| `file_path` | string | Yes | File path |
| `error_message` | string | Yes | Error message |
| `stack_trace` | string | Yes | Stack trace |
| `logs` | string | Optional | Test logs |
| `llm_model` | string | Yes | Use: `"gemma:2b"` |
| `bert_url` | string | Yes | Use: `"http://127.0.0.1:8001"` |
| `labels` | array | Optional | Labels/tags |
| `test_url` | string | Optional | URL being tested |
| `playwright_script_url` | string | Optional | Playwright script URL |

---

**Note:** The `playwright_script_url` field is where the playwright script URL should be provided.
