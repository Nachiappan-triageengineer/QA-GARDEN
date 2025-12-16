@echo off
REM Windows batch script to run Playwright tests and triage failures
REM This bypasses PowerShell execution policy issues

echo ================================================================================
echo PLAYWRIGHT TEST RUNNER (Windows)
echo ================================================================================
echo.

REM Check if node_modules exists
if not exist "node_modules" (
    echo [ERROR] node_modules not found. Installing dependencies...
    call npm install
    if errorlevel 1 (
        echo [ERROR] npm install failed
        exit /b 1
    )
)

REM Run Playwright tests with JSON reporter
echo Running Playwright tests...
echo.
call npx playwright test demo.spec.js

if errorlevel 1 (
    echo.
    echo [INFO] Tests completed with failures (this is expected for demo)
) else (
    echo.
    echo [INFO] All tests passed!
)

REM Check if report was generated
if exist "playwright-report.json" (
    echo.
    echo ================================================================================
    echo Report generated successfully!
    echo ================================================================================
    echo.
    echo Now running triage engine integration...
    echo.
    python run_playwright_and_triage.py --parse-only
) else (
    echo.
    echo [ERROR] playwright-report.json not found
    echo [TIP] Make sure playwright.config.js has JSON reporter configured
)

echo.
pause
