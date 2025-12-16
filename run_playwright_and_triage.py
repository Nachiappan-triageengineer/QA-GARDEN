"""
Playwright Test Runner & Triage Integration
Automatically runs Playwright tests and sends failures to the triage engine
"""
import subprocess
import json
import os
import requests
from pathlib import Path
from datetime import datetime

# Configuration
PLAYWRIGHT_CONFIG = "playwright.config.js"
TEST_FILE = "demo.spec.js"
REPORT_FILE = "playwright-report.json"
API_URL = "http://192.168.1.13:8003/api/triage"
LLM_MODEL = "gemma:2b"
BERT_URL = "http://localhost:8001/triage"

def run_playwright_tests():
    """Run Playwright tests and generate JSON report"""
    print("=" * 80)
    print("Running Playwright Tests")
    print("=" * 80)
    print()
    
    try:
        # Try multiple methods to run Playwright on Windows
        
        # Method 1: Use cmd.exe directly (bypasses PowerShell)
        print("Attempting to run Playwright tests...")
        result = subprocess.run(
            ["cmd", "/c", "npx playwright test demo.spec.js --reporter=json --output=playwright-report.json"],
            capture_output=True,
            text=True,
            cwd=os.getcwd()
        )
        
        print("Test execution completed!")
        print(f"Exit code: {result.returncode}")
        
        # Print stdout/stderr for debugging
        if result.stdout:
            print("\nOutput:")
            print(result.stdout[:500])
        if result.stderr:
            print("\nErrors/Warnings:")
            print(result.stderr[:500])
        
        print()
        
        # Check if report was generated
        if os.path.exists(REPORT_FILE):
            print(f"✓ Report generated: {REPORT_FILE}")
            return True
        else:
            print(f"✗ Report not found: {REPORT_FILE}")
            print("\nTroubleshooting:")
            print("1. Make sure Playwright is installed: npm install")
            print("2. Install browsers: npx playwright install")
            print("3. Try running manually: npx playwright test demo.spec.js")
            print("4. Check if playwright.config.js exists")
            return False
            
    except Exception as e:
        print(f"✗ Error running tests: {str(e)}")
        print("\nAlternative: Run Playwright manually, then use this script to parse results")
        print("  npx playwright test demo.spec.js")
        print("  python run_playwright_and_triage.py --parse-only")
        return False

def parse_playwright_report():
    """Parse the Playwright JSON report and extract failures"""
    print("\n" + "=" * 80)
    print("Parsing Test Results")
    print("=" * 80)
    print()
    
    if not os.path.exists(REPORT_FILE):
        print(f"✗ Report file not found: {REPORT_FILE}")
        return []
    
    try:
        with open(REPORT_FILE, 'r', encoding='utf-8') as f:
            report = json.load(f)
        
        failures = []
        
        # Navigate through the report structure
        for suite in report.get('suites', []):
            for spec in suite.get('specs', []):
                for test in spec.get('tests', []):
                    for result in test.get('results', []):
                        # Check if test failed
                        if result.get('status') == 'failed' or result.get('status') == 'timedOut':
                            failure = extract_failure_data(suite, spec, test, result)
                            failures.append(failure)
        
        print(f"Found {len(failures)} failed test(s)")
        return failures
        
    except Exception as e:
        print(f"✗ Error parsing report: {str(e)}")
        return []

def extract_failure_data(suite, spec, test, result):
    """Extract failure data from Playwright report"""
    # Get test name
    test_name = spec.get('title', 'Unknown Test')
    
    # Get file path
    file_path = spec.get('file', 'unknown.spec.js')
    if file_path:
        file_path = os.path.basename(file_path)
    
    # Get error message
    error = result.get('error', {})
    error_message = error.get('message', 'Test failed')
    
    # Get stack trace
    stack_trace = error.get('stack', '')
    
    # Build logs from attachments and steps
    logs = []
    logs.append(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Test: {test_name}")
    logs.append(f"Status: {result.get('status', 'unknown')}")
    logs.append(f"Duration: {result.get('duration', 0)}ms")
    
    # Add error details
    if error_message:
        logs.append(f"Error: {error_message}")
    
    # Add steps if available
    for step in result.get('steps', []):
        step_title = step.get('title', '')
        step_error = step.get('error', {}).get('message', '')
        if step_title:
            logs.append(f"  Step: {step_title}")
        if step_error:
            logs.append(f"    Error: {step_error}")
    
    logs_text = '\n'.join(logs)
    
    return {
        "test_name": test_name,
        "file_path": file_path,
        "error_message": error_message,
        "stack_trace": stack_trace,
        "logs": logs_text,
        "llm_model": LLM_MODEL,
        "bert_url": BERT_URL,
        "labels": ["playwright", "automated", "ui"]
    }

def post_to_triage_engine(failures):
    """Post failures to the triage engine API"""
    print("\n" + "=" * 80)
    print("Posting Failures to Triage Engine")
    print("=" * 80)
    print()
    
    success_count = 0
    failed_count = 0
    results = []
    
    for i, failure in enumerate(failures, 1):
        print(f"[{i}/{len(failures)}] {failure['test_name']}")
        print("-" * 80)
        
        try:
            response = requests.post(API_URL, json=failure, timeout=120)
            response.raise_for_status()
            result = response.json()
            
            print(f"✓ SUCCESS")
            print(f"  Title: {result.get('title', 'N/A')}")
            print(f"  Error Line: {result.get('error_line', 'N/A')}")
            print(f"  Playwright Script: {result.get('playwright_script', 'N/A')}")
            print(f"  ID: {result.get('id', 'N/A')}")
            
            results.append(result)
            success_count += 1
            
        except requests.exceptions.ConnectionError:
            print(f"✗ ERROR: Cannot connect to API at {API_URL}")
            print("  Make sure the triage engine is running: python main.py")
            failed_count += 1
            
        except Exception as e:
            print(f"✗ ERROR: {str(e)}")
            failed_count += 1
        
        print()
    
    print("=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"✓ Successfully triaged: {success_count}")
    print(f"✗ Failed to triage: {failed_count}")
    print(f"Total failures: {len(failures)}")
    print()
    
    return results

def main():
    """Main workflow: Run tests → Parse results → Post to triage engine"""
    import sys
    
    print("\n" + "=" * 80)
    print("PLAYWRIGHT + TRIAGE ENGINE INTEGRATION")
    print("=" * 80)
    print()
    
    # Check for parse-only mode
    parse_only = "--parse-only" in sys.argv
    
    if parse_only:
        print("Running in PARSE-ONLY mode (skipping test execution)")
        print()
    else:
        # Step 1: Run Playwright tests
        if not run_playwright_tests():
            print("\n" + "=" * 80)
            print("ALTERNATIVE WORKFLOW")
            print("=" * 80)
            print("1. Run Playwright manually in a regular command prompt:")
            print("   npx playwright test demo.spec.js")
            print()
            print("2. Then run this script in parse-only mode:")
            print("   python run_playwright_and_triage.py --parse-only")
            print("=" * 80)
            return
    
    # Step 2: Parse the report
    failures = parse_playwright_report()
    
    if not failures:
        print("\n✓ No failures found! All tests passed.")
        return
    
    # Step 3: Post to triage engine
    results = post_to_triage_engine(failures)
    
    # Step 4: Summary
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print("View triaged results with:")
    print("  python view_results.py")
    print()
    print("Or in browser:")
    print(f"  {API_URL.replace('/triage', '')}/triage")
    print("=" * 80)

if __name__ == "__main__":
    main()
