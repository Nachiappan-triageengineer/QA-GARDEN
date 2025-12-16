"""
View triage results with LOCAL PATH MAPPING

This script allows you to view test failures from others and map their file paths
to YOUR local file system, so the playwright script URLs work on your machine.
"""
import requests
import os
from urllib.parse import urlparse, unquote

API_URL = "http://192.168.1.13:8003/api/triage"

# ⭐ CONFIGURE YOUR LOCAL PATH HERE - Change this to where YOUR test files are!
YOUR_LOCAL_BASE_PATH = "C:/bug-triage-engine/tests"  # Example: "C:/my-tests" or "C:/projects/qa-tests"


def map_url_to_local_path(remote_url: str, local_base_path: str) -> str:
    """
    Convert a remote file:// URL to your local file system path.
    
    Example:
        Remote: file:///C:/their-computer/tests/login.spec.js#L14
        Local:  file:///C:/my-projects/tests/login.spec.js#L14
    """
    if not remote_url or not remote_url.startswith("file://"):
        return remote_url
    
    # Parse the URL
    parsed = urlparse(remote_url)
    remote_path = unquote(parsed.path)
    
    # Extract just the filename
    filename = os.path.basename(remote_path)
    
    # Create local path
    local_path = os.path.join(local_base_path, filename)
    
    # Convert to file:// URL
    local_url = local_path.replace('\\', '/')
    if not local_url.startswith('/'):
        local_url = '/' + local_url
    
    # Add line number anchor if present
    fragment = f"#{parsed.fragment}" if parsed.fragment else ""
    
    return f"file://{local_url}{fragment}"


print("\n" + "="*100)
print(" TRIAGE RESULTS VIEWER (WITH LOCAL PATH MAPPING)")
print("="*100)
print(f"\n[CONFIG] Your local test files path: {YOUR_LOCAL_BASE_PATH}")
print("[INFO] Remote file paths will be mapped to your local system\n")

try:
    response = requests.get(API_URL, timeout=200)
    response.raise_for_status()
    data = response.json()
    
    total = data.get("total", 0)
    results = data.get("results", [])
    
    print(f"Total Results: {total}\n")
    
    if total == 0:
        print("[INFO] No triage results found.")
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
        
        # ⭐ MAP THE PLAYWRIGHT SCRIPT URL TO YOUR LOCAL PATH
        remote_playwright_url = result.get('playwright_script', 'N/A')
        local_playwright_url = map_url_to_local_path(remote_playwright_url, YOUR_LOCAL_BASE_PATH)
        
        print(f"\n--- PLAYWRIGHT SCRIPT URLS ---")
        print(f"Remote (theirs):  {remote_playwright_url}")
        print(f"Local (yours):    {local_playwright_url}")
        print(f"\n👆 Click the LOCAL URL to open the file on YOUR system!")
        
        print(f"\nError Line:       {result.get('error_line', 'N/A')}")
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
    print("="*100)
    
    print("\n💡 TIP: Update YOUR_LOCAL_BASE_PATH at the top of this script")
    print("   to point to where YOUR test files are located.\n")
    
except requests.exceptions.ConnectionError:
    print("\n[ERROR] Cannot connect to FastAPI server at", API_URL)
    print("[TIP] Make sure FastAPI is running: python main.py")
except Exception as e:
    print(f"\n[ERROR] {str(e)}")
