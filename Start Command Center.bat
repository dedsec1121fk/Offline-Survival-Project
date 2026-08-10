@echo off
REM MAINTENANCE: Keep Command Center startup centralized in Offline Survival.py.
cd /d "%~dp0"
py -3 "Offline Survival.py" --web %*
if errorlevel 1 python "Offline Survival.py" --web %*
