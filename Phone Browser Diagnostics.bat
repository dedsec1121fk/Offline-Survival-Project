@echo off
REM MAINTENANCE: Do not hard-code a browser engine; diagnostics belong in the user-selected/default browser.
cd /d "%~dp0"
py -3 "Offline Survival.py" --phone-browser-test %*
if errorlevel 1 python "Offline Survival.py" --phone-browser-test %*
