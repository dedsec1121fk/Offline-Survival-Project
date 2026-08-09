@echo off
cd /d "%~dp0"
py -3 "Offline Survival.py" --reader %*
if errorlevel 1 python "Offline Survival.py" --reader %*
