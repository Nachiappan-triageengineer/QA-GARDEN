"""
Test script to demonstrate how to get clickable URLs from the playwright scripter
"""
import requests
import json

API_URL = "http://192.168.1.13:8003/api/triage"

# Sample failure data
sample_failure = {
    "test_name": "should display correct page title",
    "file_path": "demo.spec.js",
    "error_message": "expect(page).toHaveTitle(expected)",
    "stack_trace": "at demo.spec.js:14:5\nat WorkerRunner._runTestWithBeforeHooks",
    "logs": "[2025-12-16 10:20:00] ERROR: Title assertion failed",
    "llm_model": "gemma:2b",
    "bert_url": "http://localhost:8001/triage",
    "labels": ["playwright", "ui", "automated"],
    "test_url": "https://demo.playwright.dev/todomvc"
}


print("\n" + "="*80)
print(" TESTING CLICKABLE PLAYWRIGHT SCRIPT URL")
print("="*80)

print("\n[1] Sending test failure to triage API...")
print(f"    File path: {sample_failure['file_path']}")

try:
    response = requests.post(API_URL, json=sample_failure, timeout=200)
    response.raise_for_status()
    result = response.json()
    
    print("\n[2] [OK] Triage completed successfully!")
    print("\n" + "-"*80)
    print(" RESULT:")
    print("-"*80)
    
    print(f"\nTitle:            {result.get('title', 'N/A')}")
    print(f"Description:      {result.get('description', 'N/A')[:150]}...")
    print(f"Error Line:       {result.get('error_line', 'N/A')}")
    
    # The important part - the clickable URL!
    playwright_url = result.get('playwright_script', 'N/A')
    print(f"\n{'='*80}")
    print(" CLICKABLE PLAYWRIGHT SCRIPT URL:")
    print("="*80)
    print(f"\n{playwright_url}")
    print(f"\n{'='*80}")
    
    print("\n[3] How to use this URL:")
    print("    • Copy the URL above")
    print("    • Paste it in your browser address bar")
    print("    • Or click it if your terminal/IDE supports clickable links")
    print("    • It will open the file in your default editor or VS Code")
    
    print("\n[4] URL Format:")
    print(f"    • Protocol: file://")
    print(f"    • Full URL: {playwright_url}")
    
    # Also show how to get all results
    print("\n" + "="*80)
    print(" GETTING ALL RESULTS WITH CLICKABLE URLS")
    print("="*80)
    
    all_results = requests.get(API_URL, timeout=200)
    all_results.raise_for_status()
    data = all_results.json()
    
    print(f"\nTotal results: {data.get('total', 0)}")
    
    for i, res in enumerate(data.get('results', [])[:3], 1):  # Show first 3
        print(f"\n  [{i}] {res.get('title', 'N/A')[:50]}")
        print(f"      URL: {res.get('playwright_script', 'N/A')}")
    
    print("\n" + "="*80)
    print(" [OK] SUCCESS - URLs are now clickable!")
    print("="*80 + "\n")
    
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Cannot connect to FastAPI server")
    print("[TIP] Start the server first: python main.py")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
    import traceback
    traceback.print_exc()
