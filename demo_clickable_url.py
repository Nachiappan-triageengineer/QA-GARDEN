"""
Simple demonstration of the clickable URL feature (no server required)
"""
from app.utils.url_utils import convert_path_to_url, format_file_url_with_line

print("\n" + "="*80)
print(" CLICKABLE PLAYWRIGHT SCRIPT URL - DEMONSTRATION")
print("="*80)

# Test with different file paths
test_paths = [
    "demo.spec.js",
    "tests/login.spec.js",
    "c:\\bug-triage-engine\\demo.spec.js",
    "playwright/tests/checkout.spec.ts"
]

print("\n[1] Converting file paths to clickable URLs:\n")

for path in test_paths:
    url = convert_path_to_url(path)
    print(f"Input:  {path}")
    print(f"Output: {url}")
    print("-" * 80)

print("\n[2] Converting file paths with line numbers (NEW FEATURE!):\n")

test_paths_with_lines = [
    ("demo.spec.js", 42),
    ("tests/login.spec.js", 15),
    ("c:\\bug-triage-engine\\demo.spec.js", 123),
]

for path, line in test_paths_with_lines:
    url = format_file_url_with_line(path, line)
    print(f"Input:  {path} (line {line})")
    print(f"Output: {url}")
    print(f"Action: Ctrl+Click in VS Code to jump to line {line}")
    print("-" * 80)

print("\n[3] How to get the clickable URL from the API:")
print("""
    When you call the triage API, the response will include:
    
    {
        "title": "Bug title",
        "description": "Bug description",
        "playwright_script": "file:///C:/bug-triage-engine/demo.spec.js#L14",
        "error_line": 14,
        ...
    }
    
    Notice the #L14 anchor - this makes the URL jump to line 14 when clicked!
""")

print("[4] How to use the clickable URL:")
print("""
    • In VS Code: Ctrl+Click on the URL to open the file at the exact line
    • In terminals: Many modern terminals make file:// URLs clickable
    • In browsers: Copy and paste the URL in the address bar
    • In API clients (Postman, Insomnia): URLs are often clickable
""")

print("[5] Example usage in Python:")
print("""
    import requests
    
    response = requests.post('http://192.168.1.13:8003/api/triage', json=failure_data)
    result = response.json()
    
    # Get the clickable URL with line number
    clickable_url = result['playwright_script']
    print(f"Open this file: {clickable_url}")
    
    # The URL will look like: file:///C:/bug-triage-engine/demo.spec.js#L42
    # Ctrl+Click in VS Code to jump directly to line 42!
""")

print("="*80)
print(" ✓ URLs now include line numbers for better IDE integration!")
print("="*80 + "\n")

