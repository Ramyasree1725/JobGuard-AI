@echo off
title JobGuard AI - Create and Push 4 Git Branches
echo =======================================================
echo      JobGuard AI - Creating 4 Professional Branches
echo =======================================================
echo.

cd /d "%~dp0"

echo [1/4] Creating and pushing branch: dev ...
git checkout -B dev
git push -u origin dev

echo.
echo [2/4] Creating and pushing branch: feature/frontend-ui ...
git checkout -B feature/frontend-ui
git push -u origin feature/frontend-ui

echo.
echo [3/4] Creating and pushing branch: feature/backend-api ...
git checkout -B feature/backend-api
git push -u origin feature/backend-api

echo.
echo [4/4] Creating and pushing branch: feature/scam-heuristics ...
git checkout -B feature/scam-heuristics
git push -u origin feature/scam-heuristics

echo.
echo Returning to main branch...
git checkout main

echo.
echo =======================================================
echo   All 4 branches created and pushed to GitHub!
echo   Check: https://github.com/Ramyasree1725/JobGuard-AI/branches
echo =======================================================
pause
