@echo off
REM MAINTENANCE: Keep this launcher routed through the main Python CLI so reader behavior stays centralized.
cd /d "%~dp0"
py -3 "Offline Survival.py" --reader %*
if errorlevel 1 python "Offline Survival.py" --reader %*
