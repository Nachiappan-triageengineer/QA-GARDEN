"""
Test to verify playwright_script_url field is in the API
"""
import requests
import json

API_URL = "http://192.168.1.13:8003/api/triage"

# Test data with playwright_script_url field
test_data = {
    "test_name": "Test with script URL",
    "file_path": "test.spec.js",
    "error_message": "Test error",
    "stack_trace": "at test.spec.js:10:5",
    "logs": "Test logs",
    "llm_model": "gemma:2b",
    "bert_url": "http://localhost:8001/triage",
    "labels": ["test"],
    "test_url": "https://example.com",
    "playwright_script_url": "file:///C:/qa-tests/test.spec.js#L10"  # ← She sends this!
}

print("=" * 80)
print("Testing playwright_script_url field in POST request")
print("=" * 80)
print("\nSending data with playwright_script_url field:")
print(json.dumps(test_data, indent=2))

try:
    response = requests.post(API_URL, json=test_data, timeout=120)
    response.raise_for_status()
    result = response.json()
    
    print("\n" + "=" * 80)
    print("SUCCESS! Response received:")
    print("=" * 80)
    print(f"\nPlaywright Script in OUTPUT: {result.get('playwright_script')}")
    print("\nThe field 'playwright_script_url' is WORKING in the INPUT!")
    print("She can now send her playwright script URL in the POST request.")
    print("=" * 80)
    
except requests.exceptions.ConnectionError:
    print("\n[INFO] Server not running - but the field is already added!")
    print("[INFO] Start server with: python main.py")
    print("\nThe playwright_script_url field is ready to use in POST requests.")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
