@echo off
cd /d "%~dp0"
py -3 "Offline Survival.py" --web %*
if errorlevel 1 python "Offline Survival.py" --web %*
