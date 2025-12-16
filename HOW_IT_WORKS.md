# How the Triage Engine Works - Complete Flow

## 🔄 Data Flow Diagram

```
┌─────────────────────┐
│  Demo Failures      │
│  (Python Script)    │
└──────────┬──────────┘
           │
           │ HTTP POST Request
           │ (JSON data)
           ▼
┌─────────────────────────────────────────┐
│  FastAPI Server                         │
│  http://192.168.1.51:8003/api/triage   │
│                                         │
│  1. Receives JSON                       │
│  2. Validates with Pydantic schema      │
│  3. Calls process_failure()             │
│  4. Generates bug report (LLM)          │
│  5. Stores result in memory             │
│  6. Returns response with ID            │
└──────────┬──────────────────────────────┘
           │
           │ HTTP Response
           │ (Triage result JSON)
           ▼
┌─────────────────────┐
│  Response           │
│  {                  │
│    "title": "...",  │
│    "error_line": 14,│
│    "id": "abc123"   │
│  }                  │
└─────────────────────┘
```

## 📝 Step-by-Step: How to See It Work

### Step 1: Start the API Server

```bash
# Terminal 1 - Start the FastAPI server
cd c:\bug-triage-engine
python main.py
```

**What you'll see:**
```
INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8003 (Press CTRL+C to quit)
```

The server is now **listening** for POST requests at:
- `http://192.168.1.51:8003/api/triage` (network)
- `http://localhost:8003/api/triage` (local)

---

### Step 2: Send Data to the API

**Option A: Using the Python Script**

```bash
# Terminal 2 - Post demo failures
cd c:\bug-triage-engine
python demo_playwright_failures.py
```

**What happens internally:**
1. Script reads the 7 sample failures
2. For each failure, it does:
   ```python
   response = requests.post(
       "http://192.168.1.51:8003/api/triage",
       json=failure_data
   )
   ```
3. FastAPI receives the request
4. Processes it through `triage_service.py`
5. Returns the result

**What you'll see in Terminal 2:**
```
[1/7] Processing: should display correct page title
--------------------------------------------------------------------------------
✓ SUCCESS!
  Title: Page Title Mismatch in TodoMVC Application
  Error Line: 14
  Status: failed
  Result ID: 1702468930_abc123
```

**What you'll see in Terminal 1 (API logs):**
```
INFO:     192.168.1.51:54321 - "POST /api/triage HTTP/1.1" 200 OK
```

---

**Option B: Using cURL (Manual)**

```bash
# Send a single test failure
curl -X POST http://192.168.1.51:8003/api/triage ^
  -H "Content-Type: application/json" ^
  -d "{\"test_name\":\"test_login\",\"file_path\":\"demo.spec.js\",\"error_message\":\"Button not found\",\"stack_trace\":\"at demo.spec.js:14:5\",\"logs\":\"\",\"llm_model\":\"gemma:2b\",\"bert_url\":\"http://localhost:8001/triage\",\"labels\":[\"ui\"]}"
```

**What you'll see:**
```json
{
  "title": "Login Button Not Found",
  "description": "The test failed because...",
  "raw_failure_text": "...",
  "stack_trace": "at demo.spec.js:14:5",
  "status": "failed",
  "error_line": 14,
  "playwright_script": "demo.spec.js",
  "id": "1702468930_xyz789",
  "created_at": "2025-12-13T16:02:10"
}
```

---

### Step 3: View Stored Results

The API automatically **stores** all results in memory. You can retrieve them:

**Option A: View All Results (Python Script)**

```bash
python view_results.py
```

**What you'll see:**
```
====================================================================================================
 TRIAGE RESULTS VIEWER
====================================================================================================

Total Results: 7

====================================================================================================
 TEST #1
====================================================================================================

Title:            Page Title Mismatch in TodoMVC Application

Description:      The test expected the page title to be "Login - MyApp" but found "TodoMVC"...

--- ERROR DETAILS ---
Playwright Script: demo.spec.js
Error Line:       14
Status:           failed

--- STACK TRACE ---
    at demo.spec.js:14:5
    at WorkerRunner._runTestWithBeforeHooks...

--- METADATA ---
Created At:       2025-12-13T16:02:10
Result ID:        1702468930_abc123
```

---

**Option B: View in Browser**

Open your browser and go to:
```
http://192.168.1.51:8003/api/triage
```

You'll see JSON with all stored results:
```json
{
  "total": 7,
  "results": [
    {
      "title": "Page Title Mismatch...",
      "error_line": 14,
      "playwright_script": "demo.spec.js",
      ...
    },
    ...
  ]
}
```

---

**Option C: Get Specific Result by ID**

```bash
# Use the ID from the POST response
curl http://192.168.1.51:8003/api/triage/1702468930_abc123
```

Or in browser:
```
http://192.168.1.51:8003/api/triage/1702468930_abc123
```

---

## 🔍 How to Debug/Monitor

### See API Requests in Real-Time

**Terminal 1 (API Server)** will show:
```
INFO:     192.168.1.51:54321 - "POST /api/triage HTTP/1.1" 200 OK
INFO:     192.168.1.51:54322 - "POST /api/triage HTTP/1.1" 200 OK
INFO:     192.168.1.51:54323 - "GET /api/triage HTTP/1.1" 200 OK
```

### Check API Documentation

FastAPI auto-generates interactive docs:
```
http://192.168.1.51:8003/docs
```

This shows:
- All available endpoints
- Request/response schemas
- "Try it out" button to test directly in browser

---

## 🎯 Quick Test Commands

```bash
# 1. Start API
python main.py

# 2. (New terminal) Post demo data
python demo_playwright_failures.py

# 3. View results
python view_results.py

# 4. Or check in browser
start http://192.168.1.51:8003/api/triage
```

---

## 💡 What's Happening Behind the Scenes

When you run `python demo_playwright_failures.py`:

1. **Script prepares data:**
   ```python
   failure = {
       "test_name": "should display correct page title",
       "file_path": "demo.spec.js",
       "error_message": "expect(page).toHaveTitle...",
       "stack_trace": "at demo.spec.js:14:5",
       ...
   }
   ```

2. **Makes HTTP POST request:**
   ```python
   response = requests.post(API_URL, json=failure)
   ```

3. **FastAPI receives and processes:**
   ```python
   # In routes.py
   @router.post("/triage")
   def triage_failure(payload: FailureInput):
       result = process_failure(payload)  # Calls triage_service.py
       result_id = storage_service.store_result(result)
       return result
   ```

4. **Returns response:**
   ```json
   {
     "title": "Generated bug title",
     "error_line": 14,
     "id": "unique_id"
   }
   ```

5. **Result is stored** in memory and can be retrieved later

---

## 🚨 Troubleshooting

**Can't connect to API?**
```bash
# Check if API is running
curl http://192.168.1.51:8003/api/triage

# Or use localhost
curl http://localhost:8003/api/triage
```

**Want to see raw HTTP traffic?**
```bash
# Use verbose mode with curl
curl -v -X POST http://192.168.1.51:8003/api/triage -H "Content-Type: application/json" -d @sample_failure.json
```

That's the complete flow! 🎉
