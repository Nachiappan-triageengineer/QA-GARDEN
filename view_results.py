"""
Clean viewer for triage results - displays each test separately and clearly
"""
import requests
import json

API_URL = "http://192.168.1.13:8003/api/triage"

print("\n" + "="*100)
print(" TRIAGE RESULTS VIEWER")
print("="*100)

try:
    response = requests.get(API_URL, timeout=200)
    response.raise_for_status()
    data = response.json()
    
    total = data.get("total", 0)
    results = data.get("results", [])
    
    print(f"\nTotal Results: {total}\n")
    
    if total == 0:
        print("[INFO] No triage results found. Run convert_and_post.py first.")
        exit()
    
    for i, result in enumerate(results, 1):
        print("\n" + "="*100)
        print(f" TEST #{i}")
        print("="*100)
        
        # Basic Info
        print(f"\nTitle:            {result.get('title', 'N/A')}")
        
        desc = result.get('description', 'N/A')
        if len(desc) > 300:
            print(f"Description:      {desc[:300]}...")
        else:
            print(f"Description:      {desc}")
        
        # Error Details
        print(f"\n--- ERROR DETAILS ---")
        print(f"Test URL:         {result.get('test_url', 'N/A')}")
        print(f"Playwright Script: {result.get('playwright_script', 'N/A')}")
        print(f"Error Line:       {result.get('error_line', 'N/A')}")
        print(f"Status:           {result.get('status', 'N/A')}")
        
        # Stack Trace
        stack = result.get('stack_trace', '')
        if stack:
            print(f"\n--- STACK TRACE ---")
            if len(stack) > 500:
                print(f"{stack[:500]}...")
            else:
                print(stack)
        
        # Metadata
        print(f"\n--- METADATA ---")
        print(f"Created At:       {result.get('created_at', 'N/A')}")
        print(f"Result ID:        {result.get('id', 'N/A')}")
        
        print("\n" + "-"*100)
    
    print("\n" + "="*100)
    print(f" END OF RESULTS ({total} total)")
    print("="*100 + "\n")
    
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Cannot connect to FastAPI server at", API_URL)
    print("[TIP] Make sure FastAPI is running: python main.py")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
